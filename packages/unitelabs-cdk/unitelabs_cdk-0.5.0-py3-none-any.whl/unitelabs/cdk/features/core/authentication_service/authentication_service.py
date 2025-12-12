# ruff: noqa: D401, E501

import dataclasses
import datetime
import uuid

import typing_extensions as typing
from sila.server import FeatureIdentifier

from unitelabs.cdk import sila


class AuthenticationFailed(Exception):
    """The provided credentials are not valid."""


class InvalidAccessToken(Exception):
    """The sent access token is not valid."""


@dataclasses.dataclass
class AccessToken:
    """An access token used for authorization."""

    token: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    """The token used by the client for authorization."""

    scope: list[FeatureIdentifier] = dataclasses.field(default_factory=list)
    """The requested scope of access."""

    lifetime: datetime.timedelta = dataclasses.field(default_factory=datetime.timedelta)
    """The lifetime of the access token before it expires."""

    last_usage: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
    """Point in time when the access token was used last."""

    @property
    def is_expired(self) -> bool:
        """Whether the access token has expired."""

        return (datetime.datetime.now() - self.lifetime) > self.last_usage


class AuthenticationService(sila.Feature):
    """
    This Feature provides SiLA Clients with access tokens based on a user identification and password.

    1. the user needs to login with the Login command into the server with a user identification (=user name) and a password
    2. after verification, an Access Token with the Token Lifetime information will be generated and provided by the server.
    3. the user can log-out from the server with the Logout command - a valid Access Token is required to run this command.
    """

    def __init__(self):
        super().__init__(originator="org.silastandard", category="core")

        self.access_tokens = dict[str, AccessToken]()
        self.default_lifetime = datetime.timedelta(hours=1)

    @sila.UnobservableCommand()
    async def login(
        self,
        user_identification: str,
        password: str,
        requested_server: typing.Annotated[
            str,
            sila.constraints.Length(36),
            sila.constraints.Pattern(r"[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12}"),
        ],
        requested_features: list[
            typing.Annotated[
                str,
                sila.constraints.FullyQualifiedIdentifier("FeatureIdentifier"),
            ]
        ],
    ) -> tuple[
        str,
        typing.Annotated[int, sila.constraints.Unit("s", components=[sila.constraints.UnitComponent("Second")])],
    ]:
        """
        Provides an access token based on user information.

        Args:
          UserIdentification: The user identification string (e.g. a user
            name)
          Password: The password
          RequestedServer: The ServerUUID of the server for which an
            authorization is requested.
          RequestedFeatures: The fully qualified identifiers of features
            that are requested to access. If no feature is provided, this
            means that all features are requested.

        Returns:
          AccessToken: The token to be used along with accessing a
            Command or Property on a SiLA Server.
          TokenLifetime: The lifetime (in seconds) of the provided access
            token as the maximum validity period after the last SiLA
            Server request.

        Raises:
          AuthenticationFailed: The provided credentials are not valid.
        """

        if requested_server != self.server.uuid:
            msg = f"Requested access to server '{requested_server}' which could not be granted from server '{self.server.uuid}'."
            raise AuthenticationFailed(msg)

        features = list[FeatureIdentifier]()
        for requested_feature in requested_features:
            feature_identifier = FeatureIdentifier(requested_feature)
            features.append(feature_identifier)
            if feature_identifier not in self.server.features:
                msg = f"Requested access to unknown feature '{feature_identifier}' which could not be granted."
                raise AuthenticationFailed(msg)

        if not self.validate(user_identification, password, features):
            msg = "Received invalid credentials."
            raise AuthenticationFailed(msg)

        token = AccessToken(scope=features, lifetime=self.default_lifetime)
        self.access_tokens[token.token] = token

        return (token.token, int(token.lifetime.total_seconds()))

    @sila.UnobservableCommand()
    async def logout(self, access_token: str) -> None:
        """
        Invalidates the given access token immediately.

        Args:
          AccessToken: The access token to be invalidated.

        Raises:
          InvalidAccessToken: The sent access token is not valid.
        """

        try:
            self.access_tokens.pop(access_token)
        except KeyError:
            msg = "Received invalid or unknown token."
            raise InvalidAccessToken(msg) from None

    async def validate(self, username: str, password: str, scope: list[FeatureIdentifier]) -> bool:
        """
        Subclass to validate the given credentials.

        Args:
          username: The username.
          password: The password.
          scope: The list requested features.

        Returns:
          Whether the given username and password valid and authorized to
            access the requested scope.
        """

        raise NotImplementedError
