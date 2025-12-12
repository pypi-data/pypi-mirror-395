import dataclasses

from sila import datetime
from sila.server import (
    Any,
    Binary,
    Boolean,
    Custom,
    Date,
    Element,
    Feature,
    Integer,
    Real,
    String,
    Structure,
    Time,
    Timestamp,
    UnobservableCommand,
    UnobservableProperty,
)


@dataclasses.dataclass
class StructureDataTypeTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "StructureDataTypeTest"
    display_name: str = "Structure Data Type Test"
    description: str = (
        "Provides commands and properties to set or respectively get SiLA Structure Data Type values via command "
        "parameters or property responses respectively."
    )

    def __post_init__(self):
        test_structure = Custom.create(
            identifier="TestStructure",
            display_name="Test Structure",
            description="An example Structure data type containing all SiLA basic types.",
            data_type=Structure.create(
                {
                    "StringTypeValue": Element(
                        identifier="StringTypeValue",
                        display_name="String Type Value",
                        description="A value of SiLA data type String.",
                        data_type=String,
                    ),
                    "IntegerTypeValue": Element(
                        identifier="IntegerTypeValue",
                        display_name="Integer Type Value",
                        description="A value of SiLA data type Integer.",
                        data_type=Integer,
                    ),
                    "RealTypeValue": Element(
                        identifier="RealTypeValue",
                        display_name="Real Type Value",
                        description="A value of SiLA data type Real.",
                        data_type=Real,
                    ),
                    "BooleanTypeValue": Element(
                        identifier="BooleanTypeValue",
                        display_name="Boolean Type Value",
                        description="A value of SiLA data type Boolean.",
                        data_type=Boolean,
                    ),
                    "BinaryTypeValue": Element(
                        identifier="BinaryTypeValue",
                        display_name="Binary Type Value",
                        description="A value of SiLA data type Binary.",
                        data_type=Binary,
                    ),
                    "DateTypeValue": Element(
                        identifier="DateTypeValue",
                        display_name="Date Type Value",
                        description="A value of SiLA data type Date.",
                        data_type=Date,
                    ),
                    "TimeTypeValue": Element(
                        identifier="TimeTypeValue",
                        display_name="Time Type Value",
                        description="A value of SiLA data type Time.",
                        data_type=Time,
                    ),
                    "TimestampTypeValue": Element(
                        identifier="TimestampTypeValue",
                        display_name="Timestamp Type Value",
                        description="A value of SiLA data type Timestamp.",
                        data_type=Timestamp,
                    ),
                    "AnyTypeValue": Element(
                        identifier="AnyTypeValue",
                        display_name="Any Type Value",
                        description="A value of SiLA data type Any.",
                        data_type=Any,
                    ),
                },
            ),
        ).add_to_feature(self)

        deep_structure = Custom.create(
            identifier="DeepStructure",
            display_name="Deep Structure",
            description="An example Structure data type that contains other structures within.",
            data_type=Structure.create(
                {
                    "OuterStringTypeValue": Element(
                        identifier="OuterStringTypeValue",
                        display_name="Outer String Type Value",
                        description="A value of SiLA data type String contained in the topmost structure.",
                        data_type=String,
                    ),
                    "OuterIntegerTypeValue": Element(
                        identifier="OuterIntegerTypeValue",
                        display_name="Outer Integer Type Value",
                        description="A value of SiLA data type Integer contained in the topmost structure.",
                        data_type=Integer,
                    ),
                    "MiddleStructure": Element(
                        identifier="MiddleStructure",
                        display_name="Middle Structure",
                        description="Another structure type that is part of the outer structure.",
                        data_type=Structure.create(
                            {
                                "MiddleStringTypeValue": Element(
                                    identifier="MiddleStringTypeValue",
                                    display_name="Middle String Type Value",
                                    description="A value of SiLA data type String contained in the middle structure.",
                                    data_type=String,
                                ),
                                "MiddleIntegerTypeValue": Element(
                                    identifier="MiddleIntegerTypeValue",
                                    display_name="Middle Integer Type Value",
                                    description="A value of SiLA data type Integer contained in the middle structure.",
                                    data_type=Integer,
                                ),
                                "InnerStructure": Element(
                                    identifier="InnerStructure",
                                    display_name="Inner Structur",
                                    description="A structure type that is part of the middle structure.",
                                    data_type=Structure.create(
                                        {
                                            "InnerStringTypeValue": Element(
                                                identifier="InnerStringTypeValue",
                                                display_name="Inner String Type Value",
                                                description=(
                                                    "A value of SiLA data type String contained in the innermost "
                                                    "structure."
                                                ),
                                                data_type=String,
                                            ),
                                            "InnerIntegerTypeValue": Element(
                                                identifier="InnerIntegerTypeValue",
                                                display_name="Inner Integer Type Value",
                                                description=(
                                                    "A value of SiLA data type Integer contained in the innermost "
                                                    "structure."
                                                ),
                                                data_type=Integer,
                                            ),
                                        }
                                    ),
                                ),
                            }
                        ),
                    ),
                },
            ),
        ).add_to_feature(self)

        UnobservableCommand(
            identifier="EchoStructureValue",
            display_name="Echo Structure Value",
            description=(
                "Receives a structure value and returns the structure that has been received (binary value is expected "
                "to be an embedded value, any typer value is expected to be a Basic type)."
            ),
            parameters={
                "StructureValue": Element(
                    identifier="StructureValue",
                    display_name="Structure Value",
                    description="The Structure value to be returned.",
                    data_type=test_structure,
                ),
            },
            responses={
                "ReceivedValues": Element(
                    identifier="ReceivedValues",
                    display_name="Received Values",
                    description="The structure that has been received.",
                    data_type=test_structure,
                ),
            },
            function=lambda StructureValue, metadata: {"ReceivedValues": StructureValue},
            feature=self,
        )

        UnobservableProperty(
            identifier="StructureValue",
            display_name="Structure Value",
            description="""
                Returns a structure with the following elements values:
                - String value = 'SiLA2_Test_String_Value'
                - Integer value = 5124
                - Real value = 3.1415926
                - Boolean value = true
                - Binary value = embedded string 'SiLA2_Binary_String_Value'
                - Date value = 05.08.2022 respective 08/05/2022
                - Time value = 12:34:56.789
                - Timestamp value = 2022-08-05 12:34:56.789
                - Any type value = string 'SiLA2_Any_Type_String_Value'.
            """,
            data_type=test_structure,
            function=lambda metadata: {
                "StructureValue": {
                    "StringTypeValue": "SiLA2_Test_String_Value",
                    "IntegerTypeValue": 5124,
                    "RealTypeValue": 3.1415926,
                    "BooleanTypeValue": True,
                    "BinaryTypeValue": b"SiLA2_Binary_String_Value",
                    "DateTypeValue": datetime.date(
                        year=2022, month=8, day=5, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2))
                    ),
                    "TimeTypeValue": datetime.time(
                        hour=12,
                        minute=34,
                        second=56,
                        microsecond=789000,
                        tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2)),
                    ),
                    "TimestampTypeValue": datetime.datetime(
                        year=2022,
                        month=8,
                        day=5,
                        hour=12,
                        minute=34,
                        second=56,
                        microsecond=789000,
                        tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2)),
                    ),
                    "AnyTypeValue": "SiLA2_Any_Type_String_Value",
                }
            },
            feature=self,
        )

        UnobservableCommand(
            identifier="EchoDeepStructureValue",
            display_name="Echo Deep Structure Value",
            description="Receives a multilevel structure value and returns the structure that has been received.",
            parameters={
                "DeepStructureValue": Element(
                    identifier="DeepStructureValue",
                    display_name="DeepStructure Value",
                    description="The deep Structure value to be set.",
                    data_type=deep_structure,
                ),
            },
            responses={
                "ReceivedValues": Element(
                    identifier="ReceivedValues",
                    display_name="Received Values",
                    description="The structure that has been received.",
                    data_type=deep_structure,
                ),
            },
            function=lambda DeepStructureValue, metadata: {"ReceivedValues": DeepStructureValue},
            feature=self,
        )

        UnobservableProperty(
            identifier="DeepStructureValue",
            display_name="Deep Structure Value",
            description="""
                Returns a multilevel structure with the following values:
                - string value = 'Outer_Test_String'
                - integer value = 1111
                - middle structure value =
                - string value = 'Middle_Test_String'
                - integer value = 2222
                - inner structure value =
                    - string value = 'Inner_Test_String'
                    - integer value = 3333.
            """,
            data_type=deep_structure,
            function=lambda metadata: {
                "DeepStructureValue": {
                    "OuterStringTypeValue": "Outer_Test_String",
                    "OuterIntegerTypeValue": 1111,
                    "MiddleStructure": {
                        "MiddleStringTypeValue": "Middle_Test_String",
                        "MiddleIntegerTypeValue": 2222,
                        "InnerStructure": {
                            "InnerStringTypeValue": "Inner_Test_String",
                            "InnerIntegerTypeValue": 3333,
                        },
                    },
                }
            },
            feature=self,
        )
