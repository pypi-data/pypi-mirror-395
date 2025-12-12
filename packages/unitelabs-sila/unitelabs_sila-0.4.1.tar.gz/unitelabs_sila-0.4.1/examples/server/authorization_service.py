import dataclasses

from sila import datetime
from sila.server import DefinedExecutionError, Feature, Handler, Metadata, Server, String

InvalidAccessToken = DefinedExecutionError.create(
    identifier="InvalidAccessToken",
    display_name="Invalid Access Token",
    description="The sent access token is not valid.",
)


@dataclasses.dataclass
class AuthorizationService(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Draft"
    originator: str = "org.silastandard"
    category: str = "core"
    identifier: str = "AuthorizationService"
    display_name: str = "Authorization Service"
    description: str = """
        This Feature provides access control for the implementing server.

        It specifies the SiLA Client Metadata for the access token, that has been provided by the
        AuthenticationService core Feature.
    """

    def __post_init__(self):
        Metadata.create(
            identifier="AccessToken",
            display_name="Access Token",
            description="Token to be sent with every call in order to get access to the SiLA Server functionality.",
            data_type=String,
            affects=["org.silastandard/test/AuthenticationTest/v1"],
            function=self.intercept,
            feature=self,
        )

    async def intercept(self, access_token: str, context: Handler):
        assert isinstance(self.context, Server)

        try:
            authentication_service = self.context.get_feature("org.silastandard/core/AuthenticationService/v1")
            token = authentication_service.access_tokens[access_token]
        except KeyError:
            raise InvalidAccessToken from None
        else:
            token.last_usage = datetime.datetime.now()
