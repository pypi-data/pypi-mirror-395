import asyncio
import dataclasses

from sila import datetime
from sila.server import (
    Binary,
    CommandExecution,
    Element,
    Feature,
    List,
    Metadata,
    MetadataIdentifier,
    Native,
    ObservableCommand,
    String,
    UnobservableCommand,
    UnobservableProperty,
)

StringMetadata = Metadata.create(
    identifier="String",
    display_name="String",
    description="A string",
    data_type=String,
    affects=["org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString"],
)


@dataclasses.dataclass
class BinaryTransferTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "BinaryTransferTest"
    display_name: str = "Binary Transfer Test"
    description: str = (
        "Provides commands and properties to set or respectively get the SiLA Basic Data Type Binary via command "
        "parameters or property responses respectively."
    )

    def __post_init__(self):
        StringMetadata.add_to_feature(self)

        UnobservableCommand(
            identifier="EchoBinaryValue",
            display_name="Echo Binary Value",
            description=(
                "Receives a Binary value (transmitted either directly or via binary transfer) and returns the received "
                "value."
            ),
            parameters={
                "binary_value": Element(
                    identifier="BinaryValue",
                    display_name="Binary Value",
                    description="The Binary value to be returned.",
                    data_type=Binary,
                ),
            },
            responses={
                "received_value": Element(
                    identifier="ReceivedValue",
                    display_name="Received Value",
                    description="The received Binary value transmitted in the same way it has been received.",
                    data_type=Binary,
                ),
            },
            function=lambda binary_value, metadata: {"received_value": binary_value},
            feature=self,
        )

        ObservableCommand(
            identifier="EchoBinariesObservably",
            display_name="Echo Binaries Observably",
            description=(
                "Receives a list of binaries, echoes them individually as intermediate responses with a delay of 1 "
                "second, and then returns them as a single joint binary"
            ),
            parameters={
                "binaries": Element(
                    identifier="Binaries",
                    display_name="Binaries",
                    description="List of binaries to echo",
                    data_type=List.create(Binary),
                ),
            },
            responses={
                "joint_binary": Element(
                    identifier="JointBinary",
                    display_name="Joint Binary",
                    description="A single binary comprised of binaries received as parameter",
                    data_type=Binary,
                ),
            },
            intermediate_responses={
                "binary": Element(
                    identifier="Binary",
                    display_name="Binary",
                    description="Single binary from the parameter list",
                    data_type=Binary,
                ),
            },
            function=self.echo_binaries_observably,
            feature=self,
        )

        UnobservableProperty(
            identifier="BinaryValueDirectly",
            display_name="Binary Value Directly",
            description=(
                "Returns the UTF-8 encoded string 'SiLA2_Test_String_Value' directly transmitted as Binary value."
            ),
            data_type=Binary,
            function=lambda metadata: {"BinaryValueDirectly": b"SiLA2_Test_String_Value"},
            feature=self,
        )

        UnobservableProperty(
            identifier="BinaryValueDownload",
            display_name="Binary Value Download",
            description=(
                "Returns the Binary Transfer UUID to be used to download the binary data which is the UTF-8 encoded "
                "string 'A_slightly_longer_SiLA2_Test_String_Value_used_to_demonstrate_the_binary_download', repeated "
                "100,000 times."
            ),
            data_type=Binary,
            function=lambda metadata: {
                "BinaryValueDownload": b"A_slightly_longer_SiLA2_Test_String_Value_used_to_demonstrate_the_binary_download"
                * 100_000
            },
            feature=self,
        )

        UnobservableCommand(
            identifier="EchoBinaryAndMetadataString",
            display_name="Echo Binary And Metadata String",
            description="Receives a Binary and requires String Metadata, returns both",
            parameters={
                "binary": Element(
                    identifier="Binary",
                    display_name="Binary",
                    description="The binary to echo",
                    data_type=Binary,
                ),
            },
            responses={
                "binary": Element(
                    identifier="Binary",
                    display_name="Binary",
                    description="The received binary",
                    data_type=Binary,
                ),
                "string_metadata": Element(
                    identifier="StringMetadata",
                    display_name="String Metadata",
                    description="The received String Metadata",
                    data_type=String,
                ),
            },
            function=self.echo_binary_and_metadata_string,
            feature=self,
        )

    async def echo_binaries_observably(
        self, binaries: list[bytes], metadata: dict[MetadataIdentifier, Native], command_execution: CommandExecution
    ):
        for i, binary in enumerate(binaries):
            command_execution.update_execution_info(
                progress=(i + 1) / len(binaries),
                remaining_time=datetime.timedelta(seconds=len(binaries) - i),
            )
            command_execution.send_intermediate_responses({"binary": binary})

            await asyncio.sleep(1)

        return {"joint_binary": b"".join(binaries)}

    async def echo_binary_and_metadata_string(self, binary: bytes, metadata: dict[MetadataIdentifier, Native]):
        return {
            "binary": binary,
            "string_metadata": metadata[StringMetadata.fully_qualified_identifier()],
        }
