"""
Dataclasses and Exceptions for BasketCase.
"""

import typing
from dataclasses import dataclass, field

if typing.TYPE_CHECKING:
    from datetime import datetime


@dataclass
class Cookie:
    """
    Model for a web cookie, associated with a user.
    """

    name: str
    value: str
    user: int
    domain: str | None
    id: int | None = None


@dataclass
class User:
    """
    Model for an Instagram user and a BasketCase session.
    """

    name: str
    created: 'datetime'
    cookies: list[Cookie] = field(default_factory=list)
    id: int | None = None


@dataclass(frozen=True)
class Resource:
    """
    A remote resource (e.g. image or video), its URL and other metadata.
    """

    url: str
    id: str
    username: str


@dataclass(frozen=True)
class ResourceImage(Resource):
    """
    Resource of the image type.
    """

    extension = '.jpg'


@dataclass(frozen=True)
class ResourceVideo(Resource):
    """
    Resource of the video type.
    """

    extension = '.mp4'


@dataclass
class SessionCache:
    """
    Temporary session data.

    Attributes:
        user -- Currently active session user.
        asbd_id -- Cache for a GraphQL header value.
    """
    user: User | None = None
    asbd_id: str | None = None


class BasketCaseError(Exception):
    """
    Unspecified BasketCase error.

    Base class for BasketCase exceptions.
    """


class ExtractionError(BasketCaseError):
    """
    An error occurred during extraction of web content.
    """

class DownloadError(BasketCaseError):
    """
    An error occurred while attempting to download resources.
    """
