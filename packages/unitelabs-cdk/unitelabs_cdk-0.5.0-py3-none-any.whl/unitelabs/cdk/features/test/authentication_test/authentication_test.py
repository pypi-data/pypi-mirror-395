# ruff: noqa: D205, D401, D415, E501

import typing_extensions as typing

from unitelabs.cdk import sila

from ...core.authorization_service import AccessToken


class AuthenticationTest(sila.Feature):
    """
    Contains commands that require authentication. A client should be able to obtain an Authorization Token through the Login command of the Authentication Service feature
    using the following credentials: username: 'test', password: 'test'
    """

    def __init__(self):
        super().__init__(originator="org.silastandard", category="test")

    @sila.UnobservableCommand()
    async def requires_token(self, *, metadata: typing.Annotated[sila.Metadata, AccessToken]) -> None:
        """Requires an authorization token in order to be executed."""

    @sila.UnobservableCommand()
    def requires_token_for_binary_upload(
        self, binary_to_upload: bytes, *, metadata: typing.Annotated[sila.Metadata, AccessToken]
    ) -> None:
        """
        Requires an authorization token in order to be executed and to upload a binary parameter

        Args:
          BinaryToUpload: A binary that needs to be uploaded
        """
