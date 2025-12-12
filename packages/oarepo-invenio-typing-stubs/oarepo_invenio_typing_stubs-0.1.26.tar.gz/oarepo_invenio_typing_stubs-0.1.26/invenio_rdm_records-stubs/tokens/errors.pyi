from typing import ClassVar

from invenio_rest.errors import RESTException


class ResourceAccessTokenError(RESTException):
    code: ClassVar[int]


class MissingTokenIDError(ResourceAccessTokenError):
    description: ClassVar[str]


class InvalidTokenIDError(ResourceAccessTokenError):
    description: ClassVar[str]


class TokenDecodeError(ResourceAccessTokenError):
    description: ClassVar[str]


class InvalidTokenError(ResourceAccessTokenError):
    description: ClassVar[str]


class InvalidTokenSubjectError(ResourceAccessTokenError):
    description: ClassVar[str]


class ExpiredTokenError(InvalidTokenError):
    description: ClassVar[str]


class RATFeatureDisabledError(ResourceAccessTokenError):
    description: ClassVar[str]
