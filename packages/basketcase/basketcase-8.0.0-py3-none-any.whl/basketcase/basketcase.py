"""
Instagram media downloader.

Module containing the BasketCase class.
"""

import stat
from pathlib import Path
import logging
import io
import configparser

import httpx
from PIL import Image, UnidentifiedImageError

from basketcase.extractor import get_extractor
from basketcase.storage import Session, migrate
from basketcase.models import (
    Resource,
    ResourceImage,
    ResourceVideo,
    User,
    Cookie,
    SessionCache,
    DownloadError,
)


class BasketCase:
    """
    Find and download media from Instagram URLs.

    Main class providing methods to inspect an Instagram webpage
    and download its contents to disk.
    """

    def __init__(self, loglevel: str | None = None):
        # Setup logger
        if loglevel is None:
            loglevel = 'warning'

        numeric_level = getattr(logging, loglevel.upper(), None)

        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {loglevel}')

        logging.basicConfig(level=numeric_level)
        logging.captureWarnings(True)

        self._logger = logging.getLogger(__name__)


        # Create application data directory
        data_dir = Path.home() / '.basketcase'

        if not data_dir.exists():
            data_dir.mkdir()
            data_dir.chmod(stat.S_IRWXU)


        # Create application data files
        database_path = data_dir / 'data.db'
        database_path.touch(mode=0o0600, exist_ok=True)

        self.config_path = data_dir / 'config.ini'
        self.config = configparser.ConfigParser(allow_no_value=True)

        if not self.config_path.exists():
            self._logger.info('Config file will be created')

            self.config_path.touch(mode=0o0600)
            self.config['session'] = {
                'default_user': None
            }

            self._save_config()

        self.config.read(self.config_path)


        # Set default output directory
        self.output_dir = Path.cwd()


        # Setup HTTP client
        optional_headers = {  # To look like a browser
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) '
                          'Gecko/20100101 Firefox/140.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        self.http_client = httpx.Client(
            timeout=15.2, headers=optional_headers)


        # Setup database and session manager
        migrate(database_path)

        self.session = Session(database_path)
        self.session_cache = SessionCache()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _save_config(self):
        """
        Write configuration to file.
        """
        try:
            with open(self.config_path, mode='w', encoding='utf-8') as file:
                self.config.write(file)
        except (configparser.Error, OSError) as error:
            raise RuntimeError('Failed to save config to file.') from error

    def close(self):
        """
        Save configuration and cookies to disk, then close resources.

        Attempting to use the BasketCase instance after calling this
        method will result in errors.
        """
        self._save_config()


        # Save cookies to database
        if self.session_cache.user is not None:
            cookies = []

            for cookie in self.http_client.cookies.jar:
                cookie_ = Cookie(
                    name=cookie.name,
                    value=cookie.value,
                    domain=cookie.domain,
                    user=self.session_cache.user.id,
                )
                cookies.append(cookie_)

            self.session_cache.user.cookies = cookies
            self.session.update(self.session_cache.user)


        self.http_client.close()
        self.session.connection.close()

    def load_session(self, user: User):
        """
        Load a user's cookies into the HTTP client.
        """
        for cookie in user.cookies:
            self.http_client.cookies.set(
                name=cookie.name, value=cookie.value,
                domain=cookie.domain if cookie.domain else '')

        self.session_cache.user = user
        self._logger.info('Session %s loaded', user.id)

    def load_default_session(self):
        """
        Find and load a default session.
        """
        self._logger.info('Attempting to load a default session')

        if self.config['session']['default_user']:
            user = self.session.get_one_by_id(
                self.config['session']['default_user'])

            self.load_session(user)
        else:
            self._logger.info(
                'Default session is undefined. Checking the user list.')
            users = self.session.get_all()

            if len(users) == 0:
                self._logger.info('No sessions available')
            elif len(users) == 1:
                self._logger.info(
                    'There is only one session, so it will be loaded.')
                self.load_session(users[0])
            else:
                self._logger.info(
                    'Multiple sessions exist. None will be loaded.')

    def get(self, url: str) -> set[Resource]:
        """
        Extract downloadable material from the given URL.

        Arguments:
            url -- One of the supported URL types.
        """
        extractor = get_extractor(url, self)
        downloadable = extractor.extract()

        return downloadable

    def save(self, resource: Resource):
        """
        Download a resource and write it to the output directory.
        """
        user_dir = self.output_dir / resource.username
        user_dir.mkdir(parents=True, exist_ok=True)

        optional_headers = {  # To look like a browser
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
        }

        if isinstance(resource, ResourceImage):
            optional_headers.update({
                'Accept': 'image/avif,image/webp,image/png,image/svg+xml,'
                            'image/*;q=0.8,*/*;q=0.5',
                'Sec-Fetch-Dest': 'image',
                'Priority': 'u=5, i',
            })

        if isinstance(resource, ResourceVideo):
            optional_headers.update({
                'Sec-Fetch-Dest': 'empty',
                'Priority': 'u=4',
            })

        response = self.http_client.get(
            url=resource.url, headers=optional_headers, follow_redirects=True)
        response.raise_for_status()

        if isinstance(resource, ResourceImage):
            try:
                with Image.open(io.BytesIO(response.content)) as image:
                    image.save(user_dir / f'{resource.id}{resource.extension}')
            except UnidentifiedImageError as error:
                raise DownloadError(
                    'Failed to open and identify the image.') from error
            except OSError as error:
                raise DownloadError(
                    'Failed to convert and save the image.') from error
        elif isinstance(resource, ResourceVideo):
            with open(user_dir / f'{resource.id}{resource.extension}',
                    mode='w+b') as file:
                file.write(response.content)
        else:
            raise TypeError('Unrecognized resource type.')
