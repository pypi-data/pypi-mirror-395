import dataclasses

from sila.server import Constrained, Element, Feature, Integer, MaximalLength, String, UnobservableCommand


@dataclasses.dataclass
class UnobservableCommandTest(Feature):
    sila2_version: str = "1.0"
    version: str = "1.0"
    maturity_level: str = "Normative"
    originator: str = "org.silastandard"
    category: str = "test"
    identifier: str = "UnobservableCommandTest"
    display_name: str = "Unobservable Command Test"
    description: str = "Feature for testing unobservable commands"

    def __post_init__(self):
        UnobservableCommand(
            identifier="CommandWithoutParametersAndResponses",
            display_name="Command Without Parameters And Responses",
            description="A command that takes no parameters and returns no responses",
            function=lambda metadata: None,
            feature=self,
        )

        UnobservableCommand(
            identifier="ConvertIntegerToString",
            display_name="Convert Integer To String",
            description="A command that takes one integer parameter and returns its string representation.",
            parameters={
                "Integer": Element(
                    identifier="Integer",
                    display_name="Integer",
                    description="An integer, e.g. 12345",
                    data_type=Integer,
                ),
            },
            responses={
                "StringRepresentation": Element(
                    identifier="StringRepresentation",
                    display_name="String Representation",
                    description="The string representation of the given integer, e.g. '12345'",
                    data_type=String,
                ),
            },
            function=lambda Integer, metadata: {"StringRepresentation": str(Integer)},
            feature=self,
        )

        UnobservableCommand(
            identifier="JoinIntegerAndString",
            display_name="Join Integer And String",
            description="""
                A command which takes an integer and a string parameter and returns a string with both joined (e.g.
                "123abc")
            """,
            parameters={
                "Integer": Element(
                    identifier="Integer",
                    display_name="Integer",
                    description="An integer, e.g. 123",
                    data_type=Integer,
                ),
                "String": Element(
                    identifier="String",
                    display_name="String",
                    description="A string, e.g. 'abc'",
                    data_type=String,
                ),
            },
            responses={
                "JoinedParameters": Element(
                    identifier="JoinedParameters",
                    display_name="Joined Parameters",
                    description="Both parameters joined as string (e.g. '123abc')",
                    data_type=String,
                ),
            },
            function=lambda Integer, String, metadata: {"JoinedParameters": f"{Integer}{String}"},
            feature=self,
        )

        UnobservableCommand(
            identifier="SplitStringAfterFirstCharacter",
            display_name="Split String After First Character",
            description="""
                A command which splits a given string after its first character. Returns empty parts if the input was
                too short.
            """,
            parameters={
                "String": Element(
                    identifier="String",
                    display_name="String",
                    description="A string, e.g. 'abcde'",
                    data_type=String,
                ),
            },
            responses={
                "FirstCharacter": Element(
                    identifier="FirstCharacter",
                    display_name="First Character",
                    description="The first character, e.g. 'a', or an empty string if the input was empty",
                    data_type=Constrained.create(data_type=String, constraints=[MaximalLength(1)]),
                ),
                "Remainder": Element(
                    identifier="Remainder",
                    display_name="Remainder",
                    description=(
                        "The remainder, e.g. 'bcde', or an empty string if the input was shorter that two characters"
                    ),
                    data_type=String,
                ),
            },
            function=lambda String, metadata: {"FirstCharacter": String[:1], "Remainder": String[1:]},
            feature=self,
        )
