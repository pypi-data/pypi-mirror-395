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
    List,
    Real,
    String,
    Structure,
    Time,
    Timestamp,
    UnobservableCommand,
    UnobservableProperty,
)


@dataclasses.dataclass
class ListDataTypeTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "ListDataTypeTest"
    display_name: str = "List Data Type Test"
    description: str = (
        "Provides commands and properties to set or respectively get SiLA List Data Type values via command parameters "
        "or property responses respectively."
    )

    def __post_init__(self):
        UnobservableProperty(
            identifier="EmptyStringList",
            display_name="Empty String List",
            description="Returns an empty list of String type.",
            data_type=List.create(data_type=String),
            function=lambda metadata: {"EmptyStringList": []},
            feature=self,
        )

        UnobservableCommand(
            identifier="EchoStringList",
            display_name="Echo String List",
            description=(
                "Receives a list of string values and returns a list containing the string values that have been "
                "received."
            ),
            parameters={
                "StringList": Element(
                    identifier="StringList",
                    display_name="String List",
                    description="The list of string values to be returned.",
                    data_type=List.create(data_type=String),
                ),
            },
            responses={
                "ReceivedValues": Element(
                    identifier="ReceivedValues",
                    display_name="Received Values",
                    description="A list containing the string values that have been received.",
                    data_type=List.create(data_type=String),
                ),
            },
            function=lambda StringList, metadata: {"ReceivedValues": StringList},
            feature=self,
        )

        UnobservableProperty(
            identifier="StringList",
            display_name="String List",
            description="Returns a list with the following string values: 'SiLA 2', 'is', 'great'.",
            data_type=List.create(data_type=String),
            function=lambda metadata: {"StringList": ["SiLA 2", "is", "great"]},
            feature=self,
        )

        UnobservableCommand(
            identifier="EchoIntegerList",
            display_name="Echo Integer List",
            description=(
                "Receives a list of integer values and returns a list containing the integer values that have been "
                "received."
            ),
            parameters={
                "IntegerList": Element(
                    identifier="IntegerList",
                    display_name="Integer List",
                    description="The list of integer values to be returned.",
                    data_type=List.create(data_type=Integer),
                ),
            },
            responses={
                "ReceivedValues": Element(
                    identifier="ReceivedValues",
                    display_name="Received Values",
                    description="A list containing the integer values that have been received.",
                    data_type=List.create(data_type=Integer),
                ),
            },
            function=lambda IntegerList, metadata: {"ReceivedValues": IntegerList},
            feature=self,
        )

        UnobservableProperty(
            identifier="IntegerList",
            display_name="Integer List",
            description="Returns a list with the following integer values: 1, 2, 3.",
            data_type=List.create(data_type=Integer),
            function=lambda metadata: {"IntegerList": [1, 2, 3]},
            feature=self,
        )

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

        UnobservableCommand(
            identifier="EchoStructureList",
            display_name="Echo Structure List",
            description=(
                "Receives a list of structure values and returns a list containing the structures that have been "
                "received."
            ),
            parameters={
                "StructureList": Element(
                    identifier="StructureList",
                    display_name="Structure List",
                    description="The list of structure values to be returned.",
                    data_type=List.create(data_type=test_structure),
                ),
            },
            responses={
                "ReceivedValues": Element(
                    identifier="ReceivedValues",
                    display_name="Received Values",
                    description="A message containing the content of all structures that have been received.",
                    data_type=List.create(data_type=test_structure),
                ),
            },
            function=lambda StructureList, metadata: {"ReceivedValues": StructureList},
            feature=self,
        )

        UnobservableProperty(
            identifier="StructureList",
            display_name="Structure List",
            description=(
                """
                Returns a list with 3 structure values, whereas the values of the first element are:
                string value = 'SiLA2_Test_String_Value_1'
                integer value = 5124
                real value = 3.1415926
                boolean value = true
                binary value (embedded string) = 'Binary_String_Value_1'
                date value = 05.08.2022 respective 08/05/2022
                time value = 12:34:56.789
                time stamp value = 2022-08-05 12:34:56.789
                any type value (string) = 'Any_Type_String_Value_1'

                For the second and third element:
                the last character of the strings changes to '2' respective '3'
                the numeric values are incremented by 1
                the boolean values becomes false for element 2 and true for element 3
                for the date value day, month and year are incremented by 1
                for the time value milliseconds, seconds, minutes and hours are incremented by 1
                """
                "for the time stamp value day, month, year, milliseconds, seconds, minutes and hours are incremented "
                "by 1."
            ),
            data_type=List.create(data_type=test_structure),
            function=lambda metadata: {
                "StructureList": [
                    {
                        "StringTypeValue": "SiLA2_Test_String_Value_1",
                        "IntegerTypeValue": 5124,
                        "RealTypeValue": 3.1415926,
                        "BooleanTypeValue": True,
                        "BinaryTypeValue": b"Binary_String_Value_1",
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
                        "AnyTypeValue": "Any_Type_String_Value_1",
                    },
                    {
                        "StringTypeValue": "SiLA2_Test_String_Value_2",
                        "IntegerTypeValue": 5125,
                        "RealTypeValue": 4.1415926,
                        "BooleanTypeValue": False,
                        "BinaryTypeValue": b"Binary_String_Value_2",
                        "DateTypeValue": datetime.date(
                            year=2023, month=9, day=6, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2))
                        ),
                        "TimeTypeValue": datetime.time(
                            hour=13,
                            minute=35,
                            second=57,
                            microsecond=790000,
                            tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2)),
                        ),
                        "TimestampTypeValue": datetime.datetime(
                            year=2023,
                            month=9,
                            day=6,
                            hour=13,
                            minute=35,
                            second=57,
                            microsecond=790000,
                            tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2)),
                        ),
                        "AnyTypeValue": "Any_Type_String_Value_2",
                    },
                    {
                        "StringTypeValue": "SiLA2_Test_String_Value_3",
                        "IntegerTypeValue": 5126,
                        "RealTypeValue": 5.1415926,
                        "BooleanTypeValue": True,
                        "BinaryTypeValue": b"Binary_String_Value_3",
                        "DateTypeValue": datetime.date(
                            year=2024, month=10, day=7, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2))
                        ),
                        "TimeTypeValue": datetime.time(
                            hour=14,
                            minute=36,
                            second=58,
                            microsecond=791000,
                            tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2)),
                        ),
                        "TimestampTypeValue": datetime.datetime(
                            year=2024,
                            month=10,
                            day=7,
                            hour=14,
                            minute=36,
                            second=58,
                            microsecond=791000,
                            tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2)),
                        ),
                        "AnyTypeValue": "Any_Type_String_Value_3",
                    },
                ]
            },
            feature=self,
        )
