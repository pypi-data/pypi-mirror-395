# ruff: noqa: A002


import re

import pytest

from sila.framework.identifiers.feature_identifier import FeatureIdentifier
from sila.framework.identifiers.property_identifier import PropertyIdentifier

TEST_CASES = [
    pytest.param(
        "org.silastandard/core/SiLAService/v1/Property/ServerUUID",
        "org.silastandard",
        "core",
        "SiLAService",
        1,
        "ServerUUID",
        id="org.silastandard/core/SiLAService/v1/Property/ServerUUID",
    ),
    pytest.param(
        "org.silastandard/test/UnobservablePropertyTest/v1/Property/SecondsSince1970",
        "org.silastandard",
        "test",
        "UnobservablePropertyTest",
        1,
        "SecondsSince1970",
        id="org.silastandard/test/UnobservablePropertyTest/v1/Property/SecondsSince1970",
    ),
    pytest.param(
        "org.silastandard/test/ObservablePropertyTest/v1/Property/Alternating",
        "org.silastandard",
        "test",
        "ObservablePropertyTest",
        1,
        "Alternating",
        id="org.silastandard/test/ObservablePropertyTest/v1/Property/Alternating",
    ),
]


class TestInitialize:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    async def test_should_init_identifier_from_string(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        identifier = PropertyIdentifier(string)

        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.property == property
        assert identifier.feature_identifier == string.rpartition("/Property/")[0]

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    async def should_infer_identifier_type(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        identifier = FeatureIdentifier(string)

        assert isinstance(identifier, PropertyIdentifier)
        assert identifier == string

    async def test_should_raise_for_malformed_identifier(self):
        with pytest.raises(
            ValueError, match=re.escape("Expected fully qualified feature identifier, received 'Hello, World!'.")
        ):
            PropertyIdentifier("Hello, World!")

    async def test_should_raise_for_wrong_identifier(self):
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected fully qualified feature identifier, received 'org.silastandard/core/SiLAService/v1'."
            ),
        ):
            PropertyIdentifier("org.silastandard/core/SiLAService/v1")


class TestCreate:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    async def test_should_create_identifier_from_values(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        identifier = PropertyIdentifier.create(originator, category, feature, version, property)

        assert identifier == string
        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.property == property
        assert identifier.feature_identifier == string.rpartition("/Property/")[0]


class TestEquality:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    def test_should_compare_equality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        assert PropertyIdentifier(string) == PropertyIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    def test_should_compare_inequality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        assert (PropertyIdentifier(string) != PropertyIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    def test_should_compare_equality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        assert PropertyIdentifier(string) == string
        assert string == PropertyIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    def test_should_compare_equality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        assert (PropertyIdentifier(string) == object()) is False
        assert (object() == PropertyIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    def test_should_compare_inequality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        assert PropertyIdentifier(string) != object()
        assert object() != PropertyIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    def test_should_compare_inequality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        assert (PropertyIdentifier(string) != string) is False
        assert (string != PropertyIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    def test_should_ignore_case_comparing_equality(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        assert PropertyIdentifier(string) == string.lower()
        assert string.lower() == PropertyIdentifier(string)
        assert PropertyIdentifier(string) == string.upper()
        assert string.upper() == PropertyIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    def test_should_ignore_case_comparing_inequality(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        assert (PropertyIdentifier(string) != string.lower()) is False
        assert (string.lower() != PropertyIdentifier(string)) is False
        assert (PropertyIdentifier(string) != string.upper()) is False
        assert (string.upper() != PropertyIdentifier(string)) is False


class TestRepresentation:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "property"), TEST_CASES)
    def test_should_represent_values(
        self, string: str, originator: str, category: str, feature: str, version: int, property: str
    ):
        assert repr(PropertyIdentifier(string)) == (
            "PropertyIdentifier("
            f"value='{string}', "
            f"originator='{originator}', "
            f"category='{category}', "
            f"feature='{feature}', "
            f"version={version}, "
            f"property='{property}'"
            ")"
        )
