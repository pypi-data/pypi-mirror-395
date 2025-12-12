import dataclasses
import uuid

from sila import datetime
from sila.server import (
    Constrained,
    DefinedExecutionError,
    Element,
    Feature,
    FeatureIdentifier,
    FullyQualifiedIdentifier,
    Integer,
    Length,
    List,
    MetadataIdentifier,
    Native,
    Pattern,
    Server,
    String,
    Unit,
    UnobservableCommand,
)

AuthenticationFailed = DefinedExecutionError.create(
    identifier="AuthenticationFailed",
    display_name="Authentication Failed",
    description="The provided credentials are not valid.",
)
InvalidAccessToken = DefinedExecutionError.create(
    identifier="InvalidAccessToken",
    display_name="Invalid Access Token",
    description="The sent access token is not valid.",
)


@dataclasses.dataclass
class AccessToken:
    token: str
    features: list[FeatureIdentifier]
    lifetime_period: datetime.timedelta
    last_usage: datetime.datetime

    @property
    def remaining_lifetime(self) -> datetime.timedelta:
        return self.lifetime_period - (datetime.datetime.now() - self.last_usage)


@dataclasses.dataclass
class AuthenticationService(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Draft"
    originator: str = "org.silastandard"
    category: str = "core"
    identifier: str = "AuthenticationService"
    display_name: str = "Authentication Service"
    description: str = (
        "This Feature provides SiLA Clients with access tokens based on a user identification and password.\n"
        "1. the user needs to login with the Login command into the server with a user identification (=user name) and "
        "a password\n"
        "2. after verification, an Access Token with the Token Lifetime information will be generated and provided by "
        "the server\n."
        "3. the user can log-out from the server with the Logout command - a valid Access Token is required to run "
        "this command."
    )

    def __post_init__(self):
        self.access_tokens = dict[str, AccessToken]()

        UnobservableCommand(
            identifier="Login",
            display_name="Login",
            description="Provides an access token based on user information.",
            parameters={
                "user_identification": Element(
                    identifier="UserIdentification",
                    display_name="User Identification",
                    description="The user identification string (e.g. a user name)",
                    data_type=String,
                ),
                "password": Element(
                    identifier="Password",
                    display_name="Password",
                    description="The password",
                    data_type=String,
                ),
                "requested_server": Element(
                    identifier="RequestedServer",
                    display_name="Requested Server",
                    description="The ServerUUID of the server for which an authorization is requested.",
                    data_type=Constrained.create(
                        String,
                        [Length(36), Pattern(r"[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12}")],
                    ),
                ),
                "requested_features": Element(
                    identifier="RequestedFeatures",
                    display_name="Requested Features",
                    description=(
                        "The fully qualified identifiers of features that are requested to access. If no feature is "
                        "provided, this means that all features are requested."
                    ),
                    data_type=List.create(
                        Constrained.create(
                            data_type=String, constraints=[FullyQualifiedIdentifier("FeatureIdentifier")]
                        )
                    ),
                ),
            },
            responses={
                "access_token": Element(
                    identifier="AccessToken",
                    display_name="Access Token",
                    description="The token to be used along with accessing a Command or Property on a SiLA Server.",
                    data_type=String,
                ),
                "token_lifetime": Element(
                    identifier="TokenLifetime",
                    display_name="Token Lifetime",
                    description=(
                        "The lifetime (in seconds) of the provided access token as the maximum validity period after "
                        "the last SiLA Server request."
                    ),
                    data_type=Constrained.create(Integer, [Unit("s", components=[Unit.Component("Second")])]),
                ),
            },
            errors={AuthenticationFailed.identifier: AuthenticationFailed},
            function=self.login,
            feature=self,
        )

        UnobservableCommand(
            identifier="Logout",
            display_name="Logout",
            description="Invalidates the given access token immediately.",
            parameters={
                "access_token": Element(
                    identifier="AccessToken",
                    display_name="Access Token",
                    description="The access token to be invalidated.",
                    data_type=String,
                ),
            },
            errors={InvalidAccessToken.identifier: InvalidAccessToken},
            function=self.logout,
            feature=self,
        )

    async def login(
        self, user_identification: str, password: str, requested_server: str, requested_features: list[str], metadata
    ):
        assert isinstance(self.context, Server)

        if requested_server != self.context.uuid:
            raise AuthenticationFailed

        if (user_identification, password) != ("test", "test"):
            raise AuthenticationFailed

        features = list[FeatureIdentifier]()
        for feature_identifier in requested_features:
            feature_id = FeatureIdentifier(feature_identifier)
            features.append(feature_id)
            if feature_id not in self.context.features:
                raise AuthenticationFailed

        token = AccessToken(str(uuid.uuid4()), features, datetime.timedelta(seconds=60 * 60), datetime.datetime.now())
        self.access_tokens[token.token] = token

        return {
            "access_token": token.token,
            "token_lifetime": int(token.remaining_lifetime.total_seconds()),
        }

    async def logout(self, access_token: str, metadata: dict[MetadataIdentifier, Native]) -> None:
        try:
            self.access_tokens.pop(access_token)
        except KeyError:
            raise InvalidAccessToken from None
