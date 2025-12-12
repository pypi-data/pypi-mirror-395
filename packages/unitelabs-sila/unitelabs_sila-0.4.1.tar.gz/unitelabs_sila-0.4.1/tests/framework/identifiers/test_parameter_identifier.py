import re

import pytest

from sila.framework.identifiers.feature_identifier import FeatureIdentifier
from sila.framework.identifiers.parameter_identifier import ParameterIdentifier

TEST_CASES = [
    pytest.param(
        "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        "org.silastandard",
        "core",
        "SiLAService",
        1,
        "GetFeatureDefinition",
        "FeatureIdentifier",
        id="org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
    ),
    pytest.param(
        "org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString/Parameter/Integer",
        "org.silastandard",
        "test",
        "UnobservableCommandTest",
        1,
        "ConvertIntegerToString",
        "Integer",
        id="org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString/Parameter/Integer",
    ),
    pytest.param(
        "org.silastandard/test/ObservableCommandTest/v1/Command/Count/Parameter/N",
        "org.silastandard",
        "test",
        "ObservableCommandTest",
        1,
        "Count",
        "N",
        id="org.silastandard/test/ObservableCommandTest/v1/Command/Count/Parameter/N",
    ),
]


class TestInitialize:
    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    async def test_should_init_identifier_from_string(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        identifier = ParameterIdentifier(string)

        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.command == command
        assert identifier.parameter == parameter
        assert identifier.feature_identifier == string.rpartition("/Command/")[0]
        assert identifier.command_identifier == string.rpartition("/Parameter/")[0]

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    async def should_infer_identifier_type(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        identifier = FeatureIdentifier(string)

        assert isinstance(identifier, ParameterIdentifier)
        assert identifier == string

    async def test_should_raise_for_malformed_identifier(self):
        with pytest.raises(
            ValueError, match=re.escape("Expected fully qualified feature identifier, received 'Hello, World!'.")
        ):
            ParameterIdentifier("Hello, World!")

    async def test_should_raise_for_wrong_identifier(self):
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected fully qualified feature identifier, received 'org.silastandard/core/SiLAService/v1'."
            ),
        ):
            ParameterIdentifier("org.silastandard/core/SiLAService/v1")


class TestCreate:
    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    async def test_should_create_identifier_from_values(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        # Create identifier
        identifier = ParameterIdentifier.create(originator, category, feature, version, command, parameter)

        assert identifier == string
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.command == command
        assert identifier.feature_identifier == string.rpartition("/Command/")[0]
        assert identifier.command_identifier == string.rpartition("/Parameter/")[0]


class TestEquality:
    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    def test_should_compare_equality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        assert ParameterIdentifier(string) == ParameterIdentifier(string)

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    def test_should_compare_inequality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        assert (ParameterIdentifier(string) != ParameterIdentifier(string)) is False

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    def test_should_compare_equality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        assert ParameterIdentifier(string) == string
        assert string == ParameterIdentifier(string)

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    def test_should_compare_equality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        assert (ParameterIdentifier(string) == object()) is False
        assert (object() == ParameterIdentifier(string)) is False

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    def test_should_compare_inequality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        assert ParameterIdentifier(string) != object()
        assert object() != ParameterIdentifier(string)

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    def test_should_compare_inequality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        assert (ParameterIdentifier(string) != string) is False
        assert (string != ParameterIdentifier(string)) is False

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    def test_should_ignore_case_comparing_equality(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        assert ParameterIdentifier(string) == string.lower()
        assert string.lower() == ParameterIdentifier(string)
        assert ParameterIdentifier(string) == string.upper()
        assert string.upper() == ParameterIdentifier(string)

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    def test_should_ignore_case_comparing_inequality(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        assert (ParameterIdentifier(string) != string.lower()) is False
        assert (string.lower() != ParameterIdentifier(string)) is False
        assert (ParameterIdentifier(string) != string.upper()) is False
        assert (string.upper() != ParameterIdentifier(string)) is False


class TestRepresentation:
    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "parameter"), TEST_CASES
    )
    def test_should_represent_values(
        self, string: str, originator: str, category: str, feature: str, version: int, command: str, parameter: str
    ):
        assert repr(ParameterIdentifier(string)) == (
            "ParameterIdentifier("
            f"value='{string}', "
            f"originator='{originator}', "
            f"category='{category}', "
            f"feature='{feature}', "
            f"version={version}, "
            f"command='{command}', "
            f"parameter='{parameter}'"
            ")"
        )
