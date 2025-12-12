"""
Command-line interface for BasketCase.
"""

import argparse
import logging
from datetime import datetime
from random import randrange
from time import sleep
from pathlib import Path

from httpx import HTTPError

from basketcase import (
    BasketCase,
    User,
    Cookie,
    BasketCaseError,
)


def _session_list(args: argparse.Namespace):
    with BasketCase(loglevel=args.log) as bc:
        users = bc.session.get_all()

        for user in users:
            default = ''

            if (bc.config['session']['default_user'] is not None
                    and user.id == int(bc.config['session']['default_user'])):
                default = ' (default)'

            print(f'{user.id}: {user.name}{default}')

        raise SystemExit(0)


def _session_set_default(args: argparse.Namespace):
    with BasketCase(loglevel=args.log) as bc:
        session_id = getattr(args, 'set-default')

        user = bc.session.get_one_by_id(session_id)
        bc.config['session']['default_user'] = str(user.id)

        print(f'Session marked as default: {session_id}')
        raise SystemExit(0)


def _session_unset_default(args: argparse.Namespace):
    with BasketCase(loglevel=args.log) as bc:
        bc.config['session']['default_user'] = None

        print('Default session preference erased')
        raise SystemExit(0)


def _session_delete(args: argparse.Namespace):
    with BasketCase(loglevel=args.log) as bc:
        logger = logging.getLogger(__name__)

        user = bc.session.get_one_by_id(args.delete)
        bc.session.delete(user)

        # Database row IDs can be reused after they're deleted,
        # so clearing the preference avoids unexpected behavior.
        bc.config['session']['default_user'] = None
        logger.info('Resetting the default session preference.')

        print(f'Removed session id {args.delete}')
        raise SystemExit(0)


def _session_add_cookie(args: argparse.Namespace):
    with BasketCase(loglevel=args.log) as bc:
        logger = logging.getLogger(__name__)
        cursor = bc.session.connection.cursor()

        user = User(
            name='',
            created=datetime.now(),
        )

        if args.set_name:
            user.name = args.set_name
        else:
            user.name = input('Provide a short name to identify this session: ')

        user.id = bc.session.insert(user, cursor=cursor)
        logger.info('User created: %s', user.id)

        cookie = Cookie(
            name='sessionid',
            value=getattr(args, 'add-cookie'),
            domain=bc.session.IG_COOKIE_DOMAIN,
            user=user.id,
        )
        user.cookies.append(cookie)
        bc.session.update(user, cursor=cursor)
        bc.session.connection.commit()

        print(f'New session created (id={user.id}) '
                f'with one \'{cookie.name}\' cookie')
        raise SystemExit(0)


def _session_add_cookies(args: argparse.Namespace):
    with BasketCase(loglevel=args.log) as bc:
        logger = logging.getLogger(__name__)
        cursor = bc.session.connection.cursor()

        user = User(
            name='',
            created=datetime.now(),
        )

        if args.set_name:
            user.name = args.set_name
        else:
            user.name = input('Choose a short name to identify this session: ')

        user.id = bc.session.insert(user, cursor=cursor)
        logger.info('User created: %s', user.id)

        with open(getattr(args, 'add-cookies'),
                encoding='utf-8') as cookie_file:
            for line in cookie_file:
                for cookie in line.split(';'):
                    cookie = cookie.strip()
                    name, value = cookie.split('=', 1)
                    logger.debug('Found cookie named "%s"', name)

                    cookie_ = Cookie(
                        name=name,
                        value=value,
                        domain=bc.session.IG_COOKIE_DOMAIN,
                        user=user.id,
                    )
                    user.cookies.append(cookie_)

        bc.session.update(user, cursor=cursor)
        bc.session.connection.commit()

        print(f'New session created (id={user.id}) '
                f'with {len(user.cookies)} cookie(s)')
        raise SystemExit(0)


def main() -> int:
    """Handle command-line script execution."""

    parser = argparse.ArgumentParser(
        description='Download media from Instagram.'
    )

    parser.add_argument(
        '--log',
        help="Set logging level (see Python's standard logging library)",
        metavar='LEVEL',
        choices=['debug', 'info', 'warning', 'error', 'critical']
    )

    subparsers = parser.add_subparsers(
        title='subcommands', required=True
    )


    # get subparser
    get_parser = subparsers.add_parser(
        'get',
        help='Get command help'
    )

    get_parser.add_argument(
        'url_or_file',
        help='Download from a single URL or a text file '
                'containing a list of URLs',
        metavar='URL_OR_FILE'
    )

    get_parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Set the output directory (default is the current working '
                'directory)'
    )

    get_parser.add_argument(
        '--fast',
        help='Download as fast as possible (may trigger automated '
                'behavior warnings)',
        action='store_true'
    )


    session_group = get_parser.add_mutually_exclusive_group()

    session_group.add_argument(
        '-s', '--session',
        help='Use the specified session',
        metavar='SESSION_ID', type=int
    )

    session_group.add_argument(
        '--no-session',
        help="Don't use a session",
        action='store_true'
    )


    # session subparser
    session_parser = subparsers.add_parser(
        'session',
        help='Session management command help'
    )

    subparsers = session_parser.add_subparsers(
        title='subcommands', required=True
    )


    # session sub-command parsers
    session_list_parser = subparsers.add_parser(
        'list',
        help='Print a list of available sessions'
    )

    session_list_parser.set_defaults(action=_session_list)

    session_list_parser.add_argument(
        'list',
        help='Print a list of available sessions',
        action='store_true'
    )


    session_cookies_parser = subparsers.add_parser(
        'add-cookies',
        help='Add cookies from a file (recommended) (creates a new '
                'user session)',
        aliases=['add']
    )

    session_cookies_parser.set_defaults(action=_session_add_cookies)

    session_cookies_parser.add_argument(
        'add-cookies',
        help="A text file containing cookies in 'name=value;' format. "
            "Use your browser developer tools to copy the Cookie header.",
        metavar='FILE'
    )

    session_cookies_parser.add_argument(
        '--set-name',
        help='Set a name for the new session (your username is an adequate '
            'choice). Will be asked interactively if not specified.',
        metavar='SESSION_NAME'
    )


    session_cookie_parser = subparsers.add_parser(
        'add-cookie',
        help='Add a session cookie (creates a new user session)'
    )

    session_cookie_parser.set_defaults(action=_session_add_cookie)

    session_cookie_parser.add_argument(
        'add-cookie',
        help="The 'sessionid' cookie value",
        metavar='COOKIE_VALUE'
    )

    session_cookie_parser.add_argument(
        '--set-name',
        help='Set a name for the new session (your username is an adequate '
            'choice). Will be asked interactively if not specified.',
        metavar='SESSION_NAME'
    )


    session_del_parser = subparsers.add_parser(
        'delete',
        help='Delete a session (the user and its cookies). This will '
             'also clear the default user preference.',
        aliases=['del']
    )

    session_del_parser.set_defaults(action=_session_delete)

    session_del_parser.add_argument(
        'delete',
        help='Session identifier from the list',
        metavar='SESSION_ID', type=int
    )


    session_set_default_parser = subparsers.add_parser(
        'set-default',
        help='Mark a session as the default',
        aliases=['default']
    )

    session_set_default_parser.set_defaults(action=_session_set_default)

    session_set_default_parser.add_argument(
        'set-default',
        help='Session identifier from the list',
        metavar='SESSION_ID', type=int
    )


    session_unset_default_parser = subparsers.add_parser(
        'unset-default',
        help='Clear the default session preference',
        aliases=['clear-default', 'reset-default']
    )

    session_unset_default_parser.set_defaults(action=_session_unset_default)

    session_unset_default_parser.add_argument(
        'reset-default',
        action='store_true'
    )


    args = parser.parse_args()

    if 'action' in args:
        args.action(args)


    # Create and configure the BasketCase instance
    with BasketCase(loglevel=args.log) as bc:
        logger = logging.getLogger(__name__)

        if not args.no_session:
            if args.session:
                user = bc.session.get_one_by_id(args.session)
                bc.load_session(user)
            else:
                bc.load_default_session()

        if args.output:
            bc.output_dir = Path(args.output)


        # Populate the URL set
        urls = set()

        try:
            with open(args.url_or_file, encoding='utf-8') as file:
                for line in file:
                    line = line.rstrip()

                    if line:
                        urls.add(line)
        except OSError:
            logger.info(
                'URL_OR_FILE could not be opened as a file, '
                'so it must be a URL.')
            urls.add(args.url_or_file)
        else:
            logger.debug('URLs were retrieved from file: %s', args.url_or_file)


        # Download
        total = len(urls)
        has_errors = False

        for count, url in enumerate(urls, start=1):
            print(f'{count} of {total}: {url}')
            resources = set()

            try:
                resources = bc.get(url)
            except (HTTPError, BasketCaseError) as error:
                logger.error('%s %s', type(error), error)
                print('Failed to extract resources. Skipping this URL.')
                has_errors = True
                continue

            for resource in resources:
                print(f'Downloading: {resource.username}'
                      f'/{resource.id}{resource.extension}')

                try:
                    bc.save(resource)
                except (HTTPError, BasketCaseError) as error:
                    logger.error('%s %s', type(error), error)
                    print('Failed to download this resource. Skipping it.')
                    has_errors = True
                    continue
                finally:
                    if not args.fast:
                        # Sleep for a few seconds before the next resource
                        sleep_time = randrange(1, 6)
                        logger.debug('Sleeping for %s seconds', sleep_time)
                        sleep(sleep_time)

        if has_errors:
            return 1

        return 0


if __name__ == '__main__':
    exit_code = main()
    raise SystemExit(exit_code)
