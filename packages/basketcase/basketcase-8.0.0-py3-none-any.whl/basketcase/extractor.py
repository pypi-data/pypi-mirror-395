"""
Web scraping component of BasketCase.
"""

import re
import typing
import logging
import json
import warnings

from bs4 import BeautifulSoup

from basketcase.models import (
    Resource,
    ResourceImage,
    ResourceVideo,
    ExtractionError,
)

if typing.TYPE_CHECKING:
    import httpx

    from basketcase.basketcase import BasketCase


def get_extractor(url: str, bc: 'BasketCase') -> 'BaseExtractor':
    """
    Get a suitable extractor for the given URL.

    Raises 'ExtractionError' if it can't find an extractor.
    """
    logger = logging.getLogger(__name__)

    required_headers = {
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
    }
    optional_headers = {  # To look like a browser
        'Accept': 'text/html,application/xhtml+xml,application/xml;'
            'q=0.9,*/*;q=0.8',
        'Alt-Used': 'www.instagram.com',
        'Priority': 'u=0, i',
        'Sec-Fetch-Dest': 'document',
    }
    headers = {**required_headers, **optional_headers}

    logger.info('Attempting to find a compatible extractor for this resource.')

    response = bc.http_client.get(
        url=url, headers=headers, follow_redirects=True)
    response.raise_for_status()

    shortcode = re.search(r'"shortcode"\s*:\s*"(.*?)"', response.text)
    profile_id = re.search(r'"target_id"\s*:\s*"(.*?)"', response.text)
    highlight_id = re.search(r'"highlight_id":\s?"highlight:(.*?)"',
                            response.text)

    if profile_id is not None:
        logger.info('Looks like this is a user profile.')

        return ProfileExtractor(
            identifier=profile_id.group(1),
            bc=bc,
            html_response=response
        )

    if shortcode is not None:
        logger.info('Looks like this is a post.')

        return PostExtractor(
            identifier=shortcode.group(1),
            bc=bc,
            html_response=response
        )

    if highlight_id is not None:
        logger.info('Looks like this is a highlight.')

        return HighlightExtractor(
            identifier=highlight_id.group(1),
            bc=bc,
            html_response=response
        )

    raise ExtractionError('Failed to locate a suitable extractor '
                        f'for url: {url}')


class BaseExtractor:
    """
    Set common methods and attributes for extractors.

    Extractors should extend this class.
    """

    def __init__(
            self,
            identifier: str,
            bc: 'BasketCase',
            html_response: 'httpx.Response'):
        """
        Arguments:
            identifier -- Resource ID for the API call
                (e.g. target_id, shortcode).
            bc -- The running BasketCase instance.
            html_response -- The response from the first request
                (usually an HTML page).
        """
        self.id = identifier
        self.bc = bc
        self.html_response = html_response

        self.logger = logging.getLogger(__name__)

    def extract(self) -> set[Resource]:
        """
        Get downloadable media as a set of Resource objects.

        Extractors must override this method with their own
        implementation.
        """
        raise NotImplementedError()

    def find_best_image(
            self,
            candidates: list,
            original_width: int = None,
            original_height: int = None,
            field_name_width: str = 'width',
            field_name_height: str = 'height') -> dict:
        """
        Get the best image candidate from a list of image versions.

        The parameters "original_height" and "original_width" are
        sometimes provided by Instagram in the image metadata. If not
        specified, the largest calculated resolution is chosen.

        Sometimes the key in the metadata that corresponds to
        width and height are not named exactly "width" and "height".
        The parameters "field_name_width" and "field_name_height"
        allow you to specify the correct key.

        Returns a dictionary containing the selected image metadata.

        Arguments:
            original_height -- Usually found in the image metadata.
            original_width -- Usually found in the image metadata.
            candidates -- List of image candidates.
            field_name_width -- Override the expected key name.
            field_name_height -- Override the expected key name.
        """
        selected = candidates[0]

        for candidate in candidates:
            if ((original_height and original_width)
                    and (candidate[field_name_width] == original_width
                    and candidate[field_name_height] == original_height)):
                selected = candidate
                break

            if ((candidate[field_name_width] + candidate[field_name_height])
                    > (selected[field_name_width] + selected[field_name_height])):
                selected = candidate

        return selected

    def find_best_video(self, video_dash_manifest: str) -> str:
        """
        Extract the best video version from `video_dash_manifest`.

        NOTE: Videos extracted with this method are currently
              missing their audio stream.

        Sometimes the items `video_url` or `video_versions` don't
        contain the original (best) quality, and you end up with a
        really low resolution video that doesn't match what you see
        on a browser. The high-quality video is actually buried in
        a field named `video_dash_manifest` (an XML document).

        Returns the selected video URL.

        Arguments:
            video_dash_manifest -- The XML document as a string.
        """
        xml_soup = BeautifulSoup(video_dash_manifest, features='lxml-xml')
        representations = xml_soup.find_all('Representation',
                                            mimeType='video/mp4')

        # TODO: Merge audio and video.
        # Audio and video streams have been separated.
        #
        # audio_representation = xml_soup.find('Representation',
        #                                      mimeType='audio/mp4')

        selected = representations[0]

        for representation in representations:
            if (int(representation['height']) > int(selected['height'])
                    and int(representation['width']) > int(selected['width'])):
                selected = representation

        return selected.find('BaseURL').text

    def extract_from_item(self, item: dict, username: str) -> set[Resource]:
        """
        Extract downloadable media from a common Instagram data schema.

        Arguments:
            item -- Object describing one published media
                (e.g. story, post).
            username -- Username of the author (some items lack that
                information).
        """
        downloadable = set()

        image_version = self.find_best_image(
            candidates=item['image_versions2']['candidates'],
            original_width=item['original_width'],
            original_height=item['original_height'],
        )

        resource = ResourceImage(
            url=image_version['url'], id=item['id'], username=username)

        downloadable.add(resource)

        if item['video_versions']:
            # Apparently there's no difference in quality
            # between the versions, so we're taking the first one.
            resource = ResourceVideo(
                url=item['video_versions'][0]['url'],
                id=item['id'], username=username,
            )

            downloadable.add(resource)

        return downloadable

    def set_graphql_headers(self, headers: dict) -> dict:
        """
        Set the HTTP headers sent by the client for GraphQL requests.

        These headers are sent by the Instagram web client when calling
        a GraphQL endpoint. They may be optional, but it's important to
        have them if we want to look like a real browser.
        """
        headers.update({
            'X-IG-App-ID': '936619743392459',
        })


        csrf_token = re.search(r'"csrf_token"\s*:\s*"(.*?)"',
                                self.html_response.text)
        if csrf_token is not None:
            headers.update({
                'X-CSRFToken': csrf_token.group(1),
            })
        else:
            warnings.warn('Failed to extract X-CSRFToken.', UserWarning)


        # Extract the ASBD ID from one of the JS files included in the
        # HTML response.
        #
        # To minimize the substantial performance impact of this
        # operation, the value is only extracted once; then it's
        # cached in the BasketCase instance.

        if self.bc.session_cache.asbd_id is not None:
            self.logger.info('Reading X-ASBD-ID from cache.')
            headers.update({'X-ASBD-ID': self.bc.session_cache.asbd_id})
        else:
            html_soup = BeautifulSoup(self.html_response.text, 'lxml')
            scripts = html_soup.css.select('head > script[src][async]')

            self.logger.info(
                'Searching for X-ASBD-ID in %s script files.', len(scripts))

            for index, script in enumerate(scripts):
                response = self.bc.http_client.get(
                    url=script['src'],
                    headers={
                        'Sec-Fetch-Dest': 'script',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'cross-site'
                    }
                )

                asbd_id = re.search(r'="(.*?)";\w\.ASBD_ID=', response.text)

                if asbd_id is not None:
                    self.logger.info(
                        'X-ASBD-ID found in script index %s', index)

                    # Write to cache
                    self.bc.session_cache.asbd_id = asbd_id.group(1)

                    headers.update({'X-ASBD-ID': asbd_id.group(1)})
                    break

            if 'X-ASBD-ID' not in headers:
                warnings.warn('Failed to extract X-ASBD-ID', UserWarning)


        bloks_version = re.search(
            r'"WebBloksVersioningID",\[],{"versioningID":"(.*?)"',
            self.html_response.text)

        if bloks_version is not None:
            headers.update({'X-BLOKS-VERSION-ID': bloks_version.group(1)})
        else:
            warnings.warn('Failed to extract X-BLOKS-VERSION-ID', UserWarning)


        lsd_token = re.search(r'"LSD",\[],{"token":"(.*?)"',
                                self.html_response.text)

        if lsd_token is not None:
            headers.update({'X-FB-LSD': lsd_token.group(1)})
        else:
            warnings.warn('Failed to extract X-FB-LSD', UserWarning)


        return headers


class PostExtractor(BaseExtractor):
    """
    Extract media from traditional posts.
    """

    def extract(self):
        json_data = re.search(
            r'<script.*?>(.*?xdt_api__v1__media__shortcode__web_info.*?)</script>',
            self.html_response.text)

        if json_data is None:
            raise ExtractionError('Failed to locate the media info JSON '
                                 'in the HTML response')

        media_info = json.loads(json_data.group(1))

        media_info = (media_info['require'][0][3][0]['__bbox']['require']
                        [0][3][1]['__bbox']['result']['data']
                        ['xdt_api__v1__media__shortcode__web_info'])

        downloadable = set()

        for item in media_info['items']:
            if 'carousel_media' in item and item['carousel_media']:
                carousel_items = item['carousel_media']

                for carousel_item in carousel_items:
                    resources = self.extract_from_item(
                        carousel_item, item['user']['username'])

                    downloadable.update(resources)
            else:
                resources = self.extract_from_item(
                    item, item['user']['username'])

                downloadable.update(resources)

        return downloadable


class ProfileExtractor(BaseExtractor):
    """
    Extract media from user profiles.

    That includes recent stories and the profile picture.
    """

    def _get_profile_picture(self) -> ResourceImage:
        variables = json.dumps({
            'id': self.id,
            'render_surface': 'PROFILE',
        })
        parameters = {
            'variables': variables,
            'doc_id': '9109150515847101',
        }

        headers = {
            'Accept': '*/*',
            'Alt-Used': 'www.instagram.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-FB-Friendly-Name': 'PolarisProfilePageContentQuery',
            'X-IG-App-ID': '936619743392459',
            'X-Root-Field-Name': 'fetch__XDTUserDict',
        }
        headers = self.set_graphql_headers(headers)

        self.logger.info('Extracting the profile picture.')

        response = self.bc.http_client.post(
            url='https://www.instagram.com/graphql/query',
            data=parameters, headers=headers
        )
        response.raise_for_status()

        user_data = response.json()

        return ResourceImage(
            url=user_data['data']['user']['hd_profile_pic_url_info']['url'],
            id=user_data['data']['user']['id'],
            username=user_data['data']['user']['username'],
        )

    def _get_stories(self) -> set[Resource]:
        downloadable = set()

        variables = json.dumps({
            'reel_ids_arr': [self.id],
        })
        parameters = {
            'variables': variables,
            'doc_id': '9342251469147045',
        }

        headers = {
            'Accept': '*/*',
            'Alt-Used': 'www.instagram.com',
            'Priority': 'u=0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-FB-Friendly-Name': 'PolarisStoriesV3ReelPageStandaloneQuery',
            'X-IG-App-ID': '936619743392459',
            'X-Root-Field-Name': 'xdt_api__v1__feed__reels_media',
        }
        headers = self.set_graphql_headers(headers)

        self.logger.info('Extracting recent stories.')

        response = self.bc.http_client.post(
            url='https://www.instagram.com/graphql/query',
            data=parameters, headers=headers
        )

        response.raise_for_status()
        response_data = response.json()

        if (response_data['data']['xdt_api__v1__feed__reels_media']
                         ['reels_media']):
            reels_media = (response_data['data']
                          ['xdt_api__v1__feed__reels_media']
                          ['reels_media'][0])

            for item in reels_media['items']:
                resources = self.extract_from_item(
                    item, reels_media['user']['username'])

                downloadable.update(resources)

        return downloadable

    def extract(self):
        downloadable = set()

        if self.bc.session_cache.user is not None:
            downloadable.update(self._get_stories())

        downloadable.add(self._get_profile_picture())

        return downloadable


class HighlightExtractor(BaseExtractor):
    """
    Extract media from highlights.

    Highlights are stories that users choose to display indefinitely
    on their profile page.
    """

    def extract(self):
        downloadable = set()

        data = re.search(
            r'<script.*?>(.*?xdt_api__v1__feed__reels_media__connection.*?)</script>',
            self.html_response.text)

        if data is None:
            raise ExtractionError('Failed to locate the media info JSON '
                                 'in the HTML response')


        media_info = json.loads(data.group(1))

        media_info = (media_info['require'][0][3][0]['__bbox']['require']
                        [0][3][1]['__bbox']['result'])

        media_info = (media_info['data']
                        ['xdt_api__v1__feed__reels_media__connection'])

        node = media_info['edges'][0]['node']


        for item in node['items']:
            resources = self.extract_from_item(item, node['user']['username'])

            downloadable.update(resources)

        return downloadable
