import dataclasses
import datetime

import typing_extensions as typing

from unitelabs.cdk import sila
from unitelabs.cdk.features.core import authorization_service

from ..authentication_service import AuthenticationService


class InvalidAccessToken(Exception):
    """The sent access token is not valid."""


@dataclasses.dataclass
class AccessToken(sila.Metadatum, errors=[InvalidAccessToken]):
    """Token to be sent with every call in order to get access to the SiLA Server functionality."""

    access_token: str

    @typing.override
    async def intercept(self, context: sila.Handler) -> None:
        try:
            authentication_service = self.feature.app.get_feature(AuthenticationService)
            token = authentication_service.access_tokens[self.access_token]
        except KeyError:
            raise authorization_service.InvalidAccessToken from None
        else:
            token.last_usage = datetime.datetime.now()


class AuthorizationService(sila.Feature):
    """
    This Feature provides access control for the implementing server.

    It specifies the SiLA Client Metadata for the access token, that has been provided by the
    AuthenticationService core Feature.
    """

    def __init__(self, metadata: type[AccessToken] = AccessToken):
        super().__init__(originator="org.silastandard", category="core", metadata=[metadata])
