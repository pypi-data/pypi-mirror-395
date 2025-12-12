import dataclasses
import textwrap

from sila import datetime
from sila.server import (
    Any,
    Constrained,
    Date,
    Element,
    Feature,
    Integer,
    MetadataIdentifier,
    Native,
    Schema,
    String,
    Structure,
    UnobservableCommand,
    UnobservableProperty,
)


@dataclasses.dataclass
class AnyTypeTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "AnyTypeTest"
    display_name: str = "Any Type Test"
    description: str = (
        "Provides commands and properties to set or respectively get SiLA Any Type values via command parameters or "
        "property responses respectively."
    )

    def __post_init__(self):
        UnobservableCommand(
            identifier="SetAnyTypeValue",
            display_name="Set Any Type Value",
            description="Receives an Any type value and returns the type and the value that has been received.",
            parameters={
                "AnyTypeValue": Element(
                    identifier="AnyTypeValue",
                    display_name="Any Type Value",
                    description="The Any type value to be set.",
                    data_type=Any,
                ),
            },
            responses={
                "ReceivedAnyType": Element(
                    identifier="ReceivedAnyType",
                    display_name="Received Any Type",
                    description="The type that has been received.",
                    data_type=Constrained.create(
                        String,
                        [
                            Schema(
                                "Xml",
                                url="https://gitlab.com/SiLA2/sila_base/-/raw/beb5d703ab62b1242695f3a591f04a07ebc7b528/schema/AnyTypeDataType.xsd",
                            )
                        ],
                    ),
                ),
                "ReceivedValue": Element(
                    identifier="ReceivedValue",
                    display_name="Received Value",
                    description="The value that has been received.",
                    data_type=Any,
                ),
            },
            function=self.set_any_type_value,
            feature=self,
        )

        UnobservableProperty(
            identifier="AnyTypeStringValue",
            display_name="Any Type String Value",
            description="Returns the Any type String value 'SiLA_Any_type_of_String_type'.",
            data_type=Any,
            function=lambda metadata: {"AnyTypeStringValue": "SiLA_Any_type_of_String_type"},
            feature=self,
        )

        UnobservableProperty(
            identifier="AnyTypeIntegerValue",
            display_name="Any Type Integer Value",
            description="Returns the Any type Integer value 5124.",
            data_type=Any,
            function=lambda metadata: {"AnyTypeIntegerValue": 5124},
            feature=self,
        )

        UnobservableProperty(
            identifier="AnyTypeRealValue",
            display_name="Any Type Real Value",
            description="Returns the Any type Real value 3.1415926.",
            data_type=Any,
            function=lambda metadata: {"AnyTypeRealValue": 3.1415926},
            feature=self,
        )

        UnobservableProperty(
            identifier="AnyTypeBooleanValue",
            display_name="Any Type Boolean Value",
            description="Returns the Any type Boolean value true.",
            data_type=Any,
            function=lambda metadata: {"AnyTypeBooleanValue": True},
            feature=self,
        )

        UnobservableProperty(
            identifier="AnyTypeBinaryValue",
            display_name="Any Type Binary Value",
            description="Returns the Any type ASCII-encoded string value 'SiLA_Any_type_of_Binary_type' as Binary.",
            data_type=Any,
            function=lambda metadata: {"AnyTypeBinaryValue": b"SiLA_Any_type_of_Binary_type"},
            feature=self,
        )

        UnobservableProperty(
            identifier="AnyTypeDateValue",
            display_name="Any Type Date Value",
            description="Returns the Any type Date value 05.08.2022 respective 08/05/2022, timezone +2.",
            data_type=Any,
            function=lambda metadata: {
                "AnyTypeDateValue": datetime.date(
                    year=2022, month=8, day=5, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2))
                )
            },
            feature=self,
        )

        UnobservableProperty(
            identifier="AnyTypeTimeValue",
            display_name="Any Type Time Value",
            description="Returns the Any type Time value 12:34:56.789, timezone +2.",
            data_type=Any,
            function=lambda metadata: {
                "AnyTypeTimeValue": datetime.time(
                    hour=12,
                    minute=34,
                    second=56,
                    microsecond=789000,
                    tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2)),
                )
            },
            feature=self,
        )

        UnobservableProperty(
            identifier="AnyTypeTimestampValue",
            display_name="Any Type Timestamp Value",
            description="Returns the Any type Timestamp value 2022-08-05 12:34:56.789, timezone +2.",
            data_type=Any,
            function=lambda metadata: {
                "AnyTypeTimestampValue": datetime.datetime(
                    year=2022,
                    month=8,
                    day=5,
                    hour=12,
                    minute=34,
                    second=56,
                    microsecond=789000,
                    tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2)),
                )
            },
            feature=self,
        )

        UnobservableProperty(
            identifier="AnyTypeListValue",
            display_name="Any Type List Value",
            description="Returns the Any type String List value ('SiLA 2', 'Any', 'Type', 'String', 'List')",
            data_type=Any,
            function=lambda metadata: {"AnyTypeListValue": ["SiLA 2", "Any", "Type", "String", "List"]},
            feature=self,
        )

        UnobservableProperty(
            identifier="AnyTypeStructureValue",
            display_name="Any Type Structure Value",
            description=textwrap.dedent("""\
            Returns the following Any type Structure value:
            - String 'StringTypeValue' = 'A String value',
            - Integer 'IntegerTypeValue' = 83737665,
            - Date 'DateTypeValue' = 05.08.2022 respective 08/05/2022 timezone +2 )
            """),
            data_type=Any,
            function=self.any_type_structure_value,
            feature=self,
        )

    async def set_any_type_value(self, AnyTypeValue: Any, metadata: dict[MetadataIdentifier, Native]):
        return {
            "ReceivedAnyType": AnyTypeValue.schema,
            "ReceivedValue": AnyTypeValue.value,
        }

    async def any_type_structure_value(self, metadata):
        structure = Structure.create(
            {
                "StringTypeValue": Element(
                    identifier="StringTypeValue",
                    display_name="StringTypeValue",
                    description="Astringvalue.",
                    data_type=String,
                ),
                "IntegerTypeValue": Element(
                    identifier="IntegerTypeValue",
                    display_name="IntegerTypeValue",
                    description="Anintegervalue.",
                    data_type=Integer,
                ),
                "DateTypeValue": Element(
                    identifier="DateTypeValue",
                    display_name="DateTypeValue",
                    description="Adatevalue.",
                    data_type=Date,
                ),
            }
        )

        return {
            "AnyTypeStructureValue": await structure.from_native(
                self.context,
                {
                    "StringTypeValue": "A String value",
                    "IntegerTypeValue": 83737665,
                    "DateTypeValue": datetime.date(
                        year=2022, month=8, day=5, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2))
                    ),
                },
            )
        }
