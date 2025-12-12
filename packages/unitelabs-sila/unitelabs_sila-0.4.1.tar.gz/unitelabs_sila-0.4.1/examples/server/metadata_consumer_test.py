import dataclasses

from sila.server import (
    CommandExecution,
    Constrained,
    Element,
    Feature,
    Integer,
    Length,
    MetadataIdentifier,
    Native,
    ObservableCommand,
    ObservableProperty,
    String,
    UnobservableCommand,
    UnobservableProperty,
)

from .metadata_provider import StringMetadata, TwoIntegersMetadata


@dataclasses.dataclass
class MetadataConsumerTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "MetadataConsumerTest"
    display_name: str = "Metadata Consumer Test"
    description: str = 'This feature consumes SiLA Client Metadata from the "Metadata Provider" feature.'

    def __post_init__(self):
        ObservableCommand(
            identifier="EchoStringMetadataObservably",
            display_name="Echo String Metadata Observably",
            description=(
                'Expects the "String Metadata" metadata from the "Metadata Provider" feature and responds with the '
                "metadata value."
            ),
            responses={
                "received_string_metadata": Element(
                    identifier="ReceivedStringMetadata",
                    display_name="Received String Metadata",
                    description="The received string metadata",
                    data_type=String,
                ),
            },
            function=self.echo_string_metadata_observably,
            feature=self,
        )

        UnobservableCommand(
            identifier="EchoStringMetadata",
            display_name="Echo String Metadata",
            description=(
                'Expects the "String Metadata" metadata from the "Metadata Provider" feature and responds with the '
                "metadata value."
            ),
            responses={
                "received_string_metadata": Element(
                    identifier="ReceivedStringMetadata",
                    display_name="Received String Metadata",
                    description="The received string metadata",
                    data_type=String,
                ),
            },
            function=self.echo_string_metadata,
            feature=self,
        )

        UnobservableCommand(
            identifier="UnpackMetadata",
            display_name="Unpack Metadata",
            description=(
                'Expects the "String Metadata" and "Two Integers Metadata" metadata from the "Metadata Provider" '
                "feature and responds with all three data items."
            ),
            responses={
                "received_string": Element(
                    identifier="ReceivedString",
                    display_name="Received String",
                    description='The received string (via "String Metadata")',
                    data_type=String,
                ),
                "first_received_integer": Element(
                    identifier="FirstReceivedInteger",
                    display_name="First Received Integer",
                    description='The first element of the received integer structure (via "Two Integers Metadata")',
                    data_type=Integer,
                ),
                "second_received_integer": Element(
                    identifier="SecondReceivedInteger",
                    display_name="Second Received Integer",
                    description='The second element of the received integer structure (via "Two Integers Metadata")',
                    data_type=Integer,
                ),
            },
            function=self.unpack_metadata,
            feature=self,
        )

        UnobservableProperty(
            identifier="ReceivedStringMetadata",
            display_name="Received String Metadata",
            description=(
                'Expects the "String Metadata" metadata from the "Metadata Provider" feature and returns the metadata '
                "value."
            ),
            data_type=String,
            function=self.get_received_string_metadata,
            feature=self,
        )

        ObservableProperty(
            identifier="ReceivedStringMetadataAsCharacters",
            display_name="Received String Metadata As Characters",
            description=(
                'Expects the "String Metadata" metadata from the "Metadata Provider" feature and returns all '
                "characters of its string value as separate responses."
            ),
            data_type=Constrained.create(data_type=String, constraints=[Length(1)]),
            function=self.subscribe_received_string_metadata,
            feature=self,
        )

    async def echo_string_metadata(self, metadata: dict[MetadataIdentifier, Native]):
        return {"received_string_metadata": metadata[StringMetadata.fully_qualified_identifier()]}

    async def echo_string_metadata_observably(
        self, metadata: dict[MetadataIdentifier, Native], command_execution: CommandExecution
    ):
        return {"received_string_metadata": metadata[StringMetadata.fully_qualified_identifier()]}

    async def unpack_metadata(self, metadata: dict[MetadataIdentifier, Native]):
        return {
            "received_string": metadata[StringMetadata.fully_qualified_identifier()],
            "first_received_integer": metadata[TwoIntegersMetadata.fully_qualified_identifier()].get("first_integer"),
            "second_received_integer": metadata[TwoIntegersMetadata.fully_qualified_identifier()].get("second_integer"),
        }

    async def get_received_string_metadata(self, metadata: dict[MetadataIdentifier, Native]):
        return {"ReceivedStringMetadata": metadata[StringMetadata.fully_qualified_identifier()]}

    async def subscribe_received_string_metadata(self, metadata: dict[MetadataIdentifier, Native]):
        for char in str(metadata[StringMetadata.fully_qualified_identifier()]):
            yield {"ReceivedStringMetadataAsCharacters": char}
