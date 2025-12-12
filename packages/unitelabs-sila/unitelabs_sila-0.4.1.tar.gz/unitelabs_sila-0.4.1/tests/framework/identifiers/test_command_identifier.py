import re

import pytest

from sila.framework.identifiers.command_identifier import CommandIdentifier
from sila.framework.identifiers.feature_identifier import FeatureIdentifier

TEST_CASES = [
    pytest.param(
        "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition",
        "org.silastandard",
        "core",
        "SiLAService",
        1,
        "GetFeatureDefinition",
        id="org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition",
    ),
    pytest.param(
        "org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString",
        "org.silastandard",
        "test",
        "UnobservableCommandTest",
        1,
        "ConvertIntegerToString",
        id="org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString",
    ),
    pytest.param(
        "org.silastandard/test/ObservableCommandTest/v1/Command/Count",
        "org.silastandard",
        "test",
        "ObservableCommandTest",
        1,
        "Count",
        id="org.silastandard/test/ObservableCommandTest/v1/Command/Count",
    ),
]


class TestInitialize:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    async def test_should_init_identifier_from_string(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        identifier = CommandIdentifier(string)

        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.command == command
        assert identifier.feature_identifier == string.rpartition("/Command/")[0]
        assert identifier.command_identifier == string

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    async def should_infer_identifier_type(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        identifier = FeatureIdentifier(string)

        assert isinstance(identifier, CommandIdentifier)
        assert identifier == string

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    async def test_should_init_identifier_from_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        identifier = CommandIdentifier(FeatureIdentifier(string))

        assert isinstance(identifier, CommandIdentifier)
        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.command == command
        assert identifier.feature_identifier == string.rpartition("/Command/")[0]
        assert identifier.command_identifier == string

    async def test_should_raise_for_malformed_identifier(self):
        with pytest.raises(
            ValueError, match=re.escape("Expected fully qualified feature identifier, received 'Hello, World!'.")
        ):
            CommandIdentifier("Hello, World!")

    async def test_should_raise_for_wrong_identifier(self):
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected fully qualified feature identifier, received 'org.silastandard/core/SiLAService/v1'."
            ),
        ):
            CommandIdentifier("org.silastandard/core/SiLAService/v1")


class TestCreate:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    async def test_should_create_identifier_from_values(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        # Create identifier
        identifier = CommandIdentifier.create(originator, category, feature, version, command)

        assert identifier == string
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.command == command
        assert identifier.feature_identifier == string.rpartition("/Command/")[0]
        assert identifier.command_identifier == string


class TestEquality:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    def test_should_compare_equality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        assert CommandIdentifier(string) == CommandIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    def test_should_compare_inequality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        assert (CommandIdentifier(string) != CommandIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    def test_should_compare_equality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        assert CommandIdentifier(string) == string
        assert string == CommandIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    def test_should_compare_equality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        assert (CommandIdentifier(string) == object()) is False
        assert (object() == CommandIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    def test_should_compare_inequality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        assert CommandIdentifier(string) != object()
        assert object() != CommandIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    def test_should_compare_inequality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        assert (CommandIdentifier(string) != string) is False
        assert (string != CommandIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    def test_should_ignore_case_comparing_equality(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        assert CommandIdentifier(string) == string.lower()
        assert string.lower() == CommandIdentifier(string)
        assert CommandIdentifier(string) == string.upper()
        assert string.upper() == CommandIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    def test_should_ignore_case_comparing_inequality(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        assert (CommandIdentifier(string) != string.lower()) is False
        assert (string.lower() != CommandIdentifier(string)) is False
        assert (CommandIdentifier(string) != string.upper()) is False
        assert (string.upper() != CommandIdentifier(string)) is False


class TestRepresentation:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "command"), TEST_CASES)
    def test_should_represent_values(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str
    ):
        assert repr(CommandIdentifier(string)) == (
            "CommandIdentifier("
            f"value='{string}', "
            f"originator='{originator}', "
            f"category='{category}', "
            f"feature='{feature}', "
            f"version={version}, "
            f"command='{command}'"
            ")"
        )
