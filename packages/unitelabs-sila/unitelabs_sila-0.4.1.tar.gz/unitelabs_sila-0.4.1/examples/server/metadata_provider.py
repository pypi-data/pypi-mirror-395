import dataclasses

from sila.server import Element, Feature, Integer, Metadata, String, Structure

StringMetadata = Metadata.create(
    identifier="StringMetadata",
    display_name="String Metadata",
    description='A metadata consisting of a string. It affects the full "Metadata Consumer Test" feature.',
    data_type=String,
    affects=["org.silastandard/test/MetadataConsumerTest/v1"],
)
TwoIntegersMetadata = Metadata.create(
    identifier="TwoIntegersMetadata",
    display_name="Two Integers Metadata",
    description=(
        'A metadata consisting of a structure with two integers. It affects only the command "Unpack Metadata" '
        'of the "Metadata Consumer Test" feature.'
    ),
    data_type=Structure.create(
        {
            "first_integer": Element(
                identifier="FirstInteger",
                display_name="First Integer",
                description="The first integer",
                data_type=Integer,
            ),
            "second_integer": Element(
                identifier="SecondInteger",
                display_name="Second Integer",
                description="The second integer",
                data_type=Integer,
            ),
        }
    ),
    affects=["org.silastandard/test/MetadataConsumerTest/v1/Command/UnpackMetadata"],
)


@dataclasses.dataclass
class MetadataProvider(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "MetadataProvider"
    display_name: str = "Metadata Provider"
    description: str = 'This feature provides SiLA Client Metadata to the "Metadata Consumer Test" feature.'

    def __post_init__(self):
        StringMetadata.add_to_feature(self)
        TwoIntegersMetadata.add_to_feature(self)
