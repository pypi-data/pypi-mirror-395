# ruff: noqa: A002


import re

import pytest

from sila.framework.identifiers.feature_identifier import FeatureIdentifier
from sila.framework.identifiers.metadata_identifier import MetadataIdentifier

TEST_CASES = [
    pytest.param(
        "org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
        "org.silastandard",
        "core",
        "AuthorizationService",
        1,
        "AccessToken",
        id="org.silastandard/core/AuthorizationService/v1/Metadata/AccessToken",
    ),
]


class TestInitialize:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    async def test_should_init_identifier_from_string(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        identifier = MetadataIdentifier(string)

        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.metadata == metadata
        assert identifier.feature_identifier == string.rpartition("/Metadata/")[0]

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    async def should_infer_identifier_type(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        identifier = FeatureIdentifier(string)

        assert isinstance(identifier, MetadataIdentifier)
        assert identifier == string

    async def test_should_raise_for_malformed_identifier(self):
        with pytest.raises(
            ValueError, match=re.escape("Expected fully qualified feature identifier, received 'Hello, World!'.")
        ):
            MetadataIdentifier("Hello, World!")

    async def test_should_raise_for_wrong_identifier(self):
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected fully qualified feature identifier, received 'org.silastandard/core/SiLAService/v1'."
            ),
        ):
            MetadataIdentifier("org.silastandard/core/SiLAService/v1")


class TestCreate:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    async def test_should_create_identifier_from_values(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        identifier = MetadataIdentifier.create(originator, category, feature, version, metadata)

        assert identifier == string
        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.metadata == metadata
        assert identifier.feature_identifier == string.rpartition("/Metadata/")[0]


class TestEquality:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    def test_should_compare_equality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        assert MetadataIdentifier(string) == MetadataIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    def test_should_compare_inequality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        assert (MetadataIdentifier(string) != MetadataIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    def test_should_compare_equality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        assert MetadataIdentifier(string) == string
        assert string == MetadataIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    def test_should_compare_equality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        assert (MetadataIdentifier(string) == object()) is False
        assert (object() == MetadataIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    def test_should_compare_inequality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        assert MetadataIdentifier(string) != object()
        assert object() != MetadataIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    def test_should_compare_inequality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        assert (MetadataIdentifier(string) != string) is False
        assert (string != MetadataIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    def test_should_ignore_case_comparing_equality(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        assert MetadataIdentifier(string) == string.lower()
        assert string.lower() == MetadataIdentifier(string)
        assert MetadataIdentifier(string) == string.upper()
        assert string.upper() == MetadataIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    def test_should_ignore_case_comparing_inequality(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        assert (MetadataIdentifier(string) != string.lower()) is False
        assert (string.lower() != MetadataIdentifier(string)) is False
        assert (MetadataIdentifier(string) != string.upper()) is False
        assert (string.upper() != MetadataIdentifier(string)) is False


class TestRepresentation:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "metadata"), TEST_CASES)
    def test_should_represent_values(
        self, string: str, originator: str, category: str, feature: str, version: int, metadata: str
    ):
        assert repr(MetadataIdentifier(string)) == (
            "MetadataIdentifier("
            f"value='{string}', "
            f"originator='{originator}', "
            f"category='{category}', "
            f"feature='{feature}', "
            f"version={version}, "
            f"metadata='{metadata}'"
            ")"
        )
