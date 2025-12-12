import dataclasses

from sila import datetime
from sila.server import (
    Boolean,
    Date,
    Element,
    Feature,
    Integer,
    Real,
    String,
    Time,
    Timestamp,
    UnobservableCommand,
    UnobservableProperty,
)


@dataclasses.dataclass
class BasicDataTypesTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "BasicDataTypesTest"
    display_name: str = "Basic Data Types Test"
    description: str = (
        "Provides commands and properties to set or respectively get all SiLA Basic Data Types via command parameters "
        "or property responses respectively."
    )

    def __post_init__(self):
        UnobservableCommand(
            identifier="EchoStringValue",
            display_name="Echo String Value",
            description="Receives a String value and returns the String value that has been received.",
            parameters={
                "StringValue": Element(
                    identifier="StringValue",
                    display_name="String Value",
                    description="The String value to be returned.",
                    data_type=String,
                ),
            },
            responses={
                "ReceivedValue": Element(
                    identifier="ReceivedValue",
                    display_name="Received Value",
                    description="The String value that has been received.",
                    data_type=String,
                ),
            },
            function=lambda StringValue, metadata: {"ReceivedValue": StringValue},
            feature=self,
        )

        UnobservableProperty(
            identifier="StringValue",
            display_name="String Value",
            description="Returns the String value 'SiLA2_Test_String_Value'.",
            data_type=String,
            function=lambda metadata: {"StringValue": "SiLA2_Test_String_Value"},
            feature=self,
        )

        UnobservableCommand(
            identifier="EchoIntegerValue",
            display_name="Echo Integer Value",
            description="Receives a Integer value and returns the Integer value that has been received.",
            parameters={
                "IntegerValue": Element(
                    identifier="IntegerValue",
                    display_name="Integer Value",
                    description="The Integer value to be returned.",
                    data_type=Integer,
                ),
            },
            responses={
                "ReceivedValue": Element(
                    identifier="ReceivedValue",
                    display_name="Received Value",
                    description="The Integer value that has been received.",
                    data_type=Integer,
                ),
            },
            function=lambda IntegerValue, metadata: {"ReceivedValue": IntegerValue},
            feature=self,
        )

        UnobservableProperty(
            identifier="IntegerValue",
            display_name="Integer Value",
            description="Returns the Integer value 5124.",
            data_type=Integer,
            function=lambda metadata: {"IntegerValue": 5124},
            feature=self,
        )

        UnobservableCommand(
            identifier="EchoRealValue",
            display_name="Echo Real Value",
            description="Receives a Real value and returns the Real value that has been received.",
            parameters={
                "RealValue": Element(
                    identifier="RealValue",
                    display_name="Real Value",
                    description="The Real value to be returned.",
                    data_type=Real,
                ),
            },
            responses={
                "ReceivedValue": Element(
                    identifier="ReceivedValue",
                    display_name="Received Value",
                    description="The Real value that has been received.",
                    data_type=Real,
                ),
            },
            function=lambda RealValue, metadata: {"ReceivedValue": RealValue},
            feature=self,
        )

        UnobservableProperty(
            identifier="RealValue",
            display_name="Real Value",
            description="Returns the Real value 3.1415926.",
            data_type=Real,
            function=lambda metadata: {"RealValue": 3.1415926},
            feature=self,
        )

        UnobservableCommand(
            identifier="EchoBooleanValue",
            display_name="Echo Boolean Value",
            description="Receives a Boolean value and returns the Boolean value that has been received.",
            parameters={
                "BooleanValue": Element(
                    identifier="BooleanValue",
                    display_name="Boolean Value",
                    description="The Boolean value to be returned.",
                    data_type=Boolean,
                ),
            },
            responses={
                "ReceivedValue": Element(
                    identifier="ReceivedValue",
                    display_name="Received Value",
                    description="The Boolean value that has been received.",
                    data_type=Boolean,
                ),
            },
            function=lambda BooleanValue, metadata: {"ReceivedValue": BooleanValue},
            feature=self,
        )

        UnobservableProperty(
            identifier="BooleanValue",
            display_name="Boolean Value",
            description="Returns the Boolean value true.",
            data_type=Boolean,
            function=lambda metadata: {"BooleanValue": True},
            feature=self,
        )

        UnobservableCommand(
            identifier="EchoDateValue",
            display_name="Echo Date Value",
            description="Receives a Date value and returns the Date value that has been received.",
            parameters={
                "DateValue": Element(
                    identifier="DateValue",
                    display_name="Date Value",
                    description="The Date value to be returned.",
                    data_type=Date,
                ),
            },
            responses={
                "ReceivedValue": Element(
                    identifier="ReceivedValue",
                    display_name="Received Value",
                    description="The Date value that has been received.",
                    data_type=Date,
                ),
            },
            function=lambda DateValue, metadata: {"ReceivedValue": DateValue},
            feature=self,
        )

        UnobservableProperty(
            identifier="DateValue",
            display_name="Date Value",
            description="Returns the Date value 05.08.2022 respective 08/05/2018, timezone +2.",
            data_type=Date,
            function=lambda metadata: {
                "DateValue": datetime.date(
                    year=2022, month=8, day=5, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2))
                )
            },
            feature=self,
        )

        UnobservableCommand(
            identifier="EchoTimeValue",
            display_name="Echo Time Value",
            description="Receives a Time value and returns the Time value that has been received.",
            parameters={
                "TimeValue": Element(
                    identifier="TimeValue",
                    display_name="Time Value",
                    description="The Time value to be returned.",
                    data_type=Time,
                ),
            },
            responses={
                "ReceivedValue": Element(
                    identifier="ReceivedValue",
                    display_name="Received Value",
                    description="The Time value that has been received.",
                    data_type=Time,
                ),
            },
            function=lambda TimeValue, metadata: {"ReceivedValue": TimeValue},
            feature=self,
        )

        UnobservableProperty(
            identifier="TimeValue",
            display_name="Time Value",
            description="Returns the Time value 12:34:56.789, timezone +2.",
            data_type=Time,
            function=lambda metadata: {
                "TimeValue": datetime.time(
                    hour=12,
                    minute=34,
                    second=56,
                    microsecond=789000,
                    tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2)),
                )
            },
            feature=self,
        )

        UnobservableCommand(
            identifier="EchoTimestampValue",
            display_name="Echo Timestamp Value",
            description="Receives a Timestamp value and returns the Timestamp value that has been received.",
            parameters={
                "TimestampValue": Element(
                    identifier="TimestampValue",
                    display_name="Timestamp Value",
                    description="The Timestamp value to be returned.",
                    data_type=Timestamp,
                ),
            },
            responses={
                "ReceivedValue": Element(
                    identifier="ReceivedValue",
                    display_name="Received Value",
                    description="The Timestamp value that has been received.",
                    data_type=Timestamp,
                ),
            },
            function=lambda TimestampValue, metadata: {"ReceivedValue": TimestampValue},
            feature=self,
        )

        UnobservableProperty(
            identifier="TimestampValue",
            display_name="Timestamp Value",
            description="Returns the Timestamp value 2022-08-05 12:34:56.789, timezone +2.",
            data_type=Timestamp,
            function=lambda metadata: {
                "TimestampValue": datetime.datetime(
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
