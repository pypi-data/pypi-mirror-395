# ruff: noqa: A002


import re

import pytest

from sila.framework.identifiers.error_identifier import ErrorIdentifier
from sila.framework.identifiers.feature_identifier import FeatureIdentifier

TEST_CASES = [
    pytest.param(
        "org.silastandard/core/SiLAService/v1/DefinedExecutionError/UnimplementedFeature",
        "org.silastandard",
        "core",
        "SiLAService",
        1,
        "UnimplementedFeature",
        id="org.silastandard/core/SiLAService/v1/DefinedExecutionError/UnimplementedFeature",
    ),
    pytest.param(
        "org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError",
        "org.silastandard",
        "test",
        "ErrorHandlingTest",
        1,
        "TestError",
        id="org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError",
    ),
]


class TestInitialize:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    async def test_should_init_identifier_from_string(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        identifier = ErrorIdentifier(string)

        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.error == error
        assert identifier.feature_identifier == string.rpartition("/DefinedExecutionError/")[0]

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    async def should_infer_identifier_type(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        identifier = FeatureIdentifier(string)

        assert isinstance(identifier, ErrorIdentifier)
        assert identifier == string

    async def test_should_raise_for_malformed_identifier(self):
        with pytest.raises(
            ValueError, match=re.escape("Expected fully qualified feature identifier, received 'Hello, World!'.")
        ):
            ErrorIdentifier("Hello, World!")

    async def test_should_raise_for_wrong_identifier(self):
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected fully qualified feature identifier, received 'org.silastandard/core/SiLAService/v1'."
            ),
        ):
            ErrorIdentifier("org.silastandard/core/SiLAService/v1")


class TestCreate:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    async def test_should_create_identifier_from_values(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        identifier = ErrorIdentifier.create(originator, category, feature, version, error)

        assert identifier == string
        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.error == error
        assert identifier.feature_identifier == string.rpartition("/DefinedExecutionError/")[0]


class TestEquality:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    def test_should_compare_equality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        assert ErrorIdentifier(string) == ErrorIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    def test_should_compare_inequality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        assert (ErrorIdentifier(string) != ErrorIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    def test_should_compare_equality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        assert ErrorIdentifier(string) == string
        assert string == ErrorIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    def test_should_compare_equality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        assert (ErrorIdentifier(string) == object()) is False
        assert (object() == ErrorIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    def test_should_compare_inequality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        assert ErrorIdentifier(string) != object()
        assert object() != ErrorIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    def test_should_compare_inequality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        assert (ErrorIdentifier(string) != string) is False
        assert (string != ErrorIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    def test_should_ignore_case_comparing_equality(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        assert ErrorIdentifier(string) == string.lower()
        assert string.lower() == ErrorIdentifier(string)
        assert ErrorIdentifier(string) == string.upper()
        assert string.upper() == ErrorIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    def test_should_ignore_case_comparing_inequality(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        assert (ErrorIdentifier(string) != string.lower()) is False
        assert (string.lower() != ErrorIdentifier(string)) is False
        assert (ErrorIdentifier(string) != string.upper()) is False
        assert (string.upper() != ErrorIdentifier(string)) is False


class TestRepresentation:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "error"), TEST_CASES)
    def test_should_represent_values(
        self, string: str, originator: str, category: str, feature: str, version: int, error: str
    ):
        assert repr(ErrorIdentifier(string)) == (
            "ErrorIdentifier("
            f"value='{string}', "
            f"originator='{originator}', "
            f"category='{category}', "
            f"feature='{feature}', "
            f"version={version}, "
            f"error='{error}'"
            ")"
        )
