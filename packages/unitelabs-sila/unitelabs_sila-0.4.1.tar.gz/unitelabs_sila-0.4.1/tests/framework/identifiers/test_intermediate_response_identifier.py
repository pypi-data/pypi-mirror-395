import re

import pytest

from sila.framework.identifiers.feature_identifier import FeatureIdentifier
from sila.framework.identifiers.intermediate_response_identifier import IntermediateResponseIdentifier

TEST_CASES = [
    pytest.param(
        "org.silastandard/test/ObservableCommandTest/v1/Command/Count/IntermediateResponse/CurrentIteration",
        "org.silastandard",
        "test",
        "ObservableCommandTest",
        1,
        "Count",
        "CurrentIteration",
        id="org.silastandard/test/ObservableCommandTest/v1/Command/Count/IntermediateResponse/CurrentIteration",
    ),
]


class TestInitialize:
    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    async def test_should_init_identifier_from_string(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        identifier = IntermediateResponseIdentifier(string)

        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.command == command
        assert identifier.intermediate_response == intermediate_response
        assert identifier.feature_identifier == string.rpartition("/Command/")[0]
        assert identifier.command_identifier == string.rpartition("/IntermediateResponse/")[0]

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    async def should_infer_identifier_type(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        identifier = FeatureIdentifier(string)

        assert isinstance(identifier, IntermediateResponseIdentifier)
        assert identifier == string

    async def test_should_raise_for_malformed_identifier(self):
        with pytest.raises(
            ValueError, match=re.escape("Expected fully qualified feature identifier, received 'Hello, World!'.")
        ):
            IntermediateResponseIdentifier("Hello, World!")

    async def test_should_raise_for_wrong_identifier(self):
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected fully qualified feature identifier, received 'org.silastandard/core/SiLAService/v1'."
            ),
        ):
            IntermediateResponseIdentifier("org.silastandard/core/SiLAService/v1")


class TestCreate:
    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    async def test_should_create_identifier_from_values(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        # Create identifier
        identifier = IntermediateResponseIdentifier.create(
            originator, category, feature, version, command, intermediate_response
        )

        assert identifier == string
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.command == command
        assert identifier.feature_identifier == string.rpartition("/Command/")[0]
        assert identifier.command_identifier == string.rpartition("/IntermediateResponse/")[0]


class TestEquality:
    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    def test_should_compare_equality_to_identifier(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        assert IntermediateResponseIdentifier(string) == IntermediateResponseIdentifier(string)

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    def test_should_compare_inequality_to_identifier(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        assert (IntermediateResponseIdentifier(string) != IntermediateResponseIdentifier(string)) is False

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    def test_should_compare_equality_to_string(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        assert IntermediateResponseIdentifier(string) == string
        assert string == IntermediateResponseIdentifier(string)

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    def test_should_compare_equality_to_non_string(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        assert (IntermediateResponseIdentifier(string) == object()) is False
        assert (object() == IntermediateResponseIdentifier(string)) is False

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    def test_should_compare_inequality_to_non_string(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        assert IntermediateResponseIdentifier(string) != object()
        assert object() != IntermediateResponseIdentifier(string)

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    def test_should_compare_inequality_to_string(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        assert (IntermediateResponseIdentifier(string) != string) is False
        assert (string != IntermediateResponseIdentifier(string)) is False

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    def test_should_ignore_case_comparing_equality(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        assert IntermediateResponseIdentifier(string) == string.lower()
        assert string.lower() == IntermediateResponseIdentifier(string)
        assert IntermediateResponseIdentifier(string) == string.upper()
        assert string.upper() == IntermediateResponseIdentifier(string)

    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    def test_should_ignore_case_comparing_inequality(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        assert (IntermediateResponseIdentifier(string) != string.lower()) is False
        assert (string.lower() != IntermediateResponseIdentifier(string)) is False
        assert (IntermediateResponseIdentifier(string) != string.upper()) is False
        assert (string.upper() != IntermediateResponseIdentifier(string)) is False


class TestRepresentation:
    @pytest.mark.parametrize(
        ("string", "originator", "category", "feature", "version", "command", "intermediate_response"), TEST_CASES
    )
    def test_should_represent_values(
        self,
        string: str,
        originator: str,
        category: str,
        feature: str,
        version: int,
        command: str,
        intermediate_response: str,
    ):
        assert repr(IntermediateResponseIdentifier(string)) == (
            "IntermediateResponseIdentifier("
            f"value='{string}', "
            f"originator='{originator}', "
            f"category='{category}', "
            f"feature='{feature}', "
            f"version={version}, "
            f"command='{command}', "
            f"intermediate_response='{intermediate_response}'"
            ")"
        )
