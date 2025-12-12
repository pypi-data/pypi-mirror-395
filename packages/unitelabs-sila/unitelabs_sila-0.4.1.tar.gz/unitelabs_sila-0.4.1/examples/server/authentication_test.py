import dataclasses

from sila.server import Binary, Element, Feature, UnobservableCommand


@dataclasses.dataclass
class AuthenticationTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "AuthenticationTest"
    display_name: str = "Authentication Test"
    description: str = (
        "Contains commands that require authentication. A client should be able to obtain an Authorization Token "
        "through the Login command of the Authentication Service feature using the following credentials: username: "
        "'test', password: 'test'"
    )

    def __post_init__(self):
        UnobservableCommand(
            identifier="RequiresToken",
            display_name="Requires Token",
            description="Requires an authorization token in order to be executed",
            feature=self,
        )

        UnobservableCommand(
            identifier="RequiresTokenForBinaryUpload",
            display_name="Requires Token For Binary Upload",
            description="Requires an authorization token in order to be executed and to upload a binary parameter",
            parameters={
                "binary_to_upload": Element(
                    identifier="BinaryToUpload",
                    display_name="Binary To Upload",
                    description="A binary that needs to be uploaded",
                    data_type=Binary,
                )
            },
            feature=self,
        )
