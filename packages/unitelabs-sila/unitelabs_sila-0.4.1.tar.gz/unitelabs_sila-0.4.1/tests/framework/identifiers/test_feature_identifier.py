import re

import pytest

from sila.framework.identifiers.feature_identifier import FeatureIdentifier

TEST_CASES = [
    pytest.param(
        "org.silastandard/core/SiLAService/v1",
        "org.silastandard",
        "core",
        "SiLAService",
        1,
        id="org.silastandard/core/SiLAService/v1",
    ),
    pytest.param(
        "org.silastandard/core/LockController/v2",
        "org.silastandard",
        "core",
        "LockController",
        2,
        id="org.silastandard/core/LockController/v2",
    ),
    pytest.param(
        "org.silastandard/examples/GreetingProvider/v1",
        "org.silastandard",
        "examples",
        "GreetingProvider",
        1,
        id="org.silastandard/examples/GreetingProvider/v1",
    ),
    pytest.param(
        "org.sila2standard/number/NumberProvider/v1",
        "org.sila2standard",
        "number",
        "NumberProvider",
        1,
        id="org.sila2standard/number/NumberProvider/v1",
    ),
    pytest.param(
        "org2.silastandard/number/NumberProvider/v1",
        "org2.silastandard",
        "number",
        "NumberProvider",
        1,
        id="org2.sila2standard/number/NumberProvider/v1",
    ),
    pytest.param(
        "org.silastandard/number9/NumberProvider/v1",
        "org.silastandard",
        "number9",
        "NumberProvider",
        1,
        id="org.silastandard/number9/NumberProvider/v1",
    ),
    pytest.param(
        "org.silastandard/number.n9/NumberProvider/v2",
        "org.silastandard",
        "number.n9",
        "NumberProvider",
        2,
        id="org.silastandard/number.n9/NumberProvider/v2",
    ),
]

INVALID_TEST_CASES = [
    pytest.param(
        "org.silastandard/number.9/NumberProvider/v1",
        id="category",
    ),
    pytest.param(
        "org.2silastandard/number.n9/NumberProvider/v2",
        id="originator",
    ),
]


class TestInitialize:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    async def test_should_init_identifier_from_string(
        self, string: str, originator: str, category: str, feature: str, version: int
    ):
        identifier = FeatureIdentifier(string)

        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.feature_identifier == string

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    async def test_should_init_identifier_from_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int
    ):
        identifier = FeatureIdentifier(FeatureIdentifier(string))

        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.feature_identifier == string

    async def test_should_raise_for_malformed_identifier(self):
        with pytest.raises(
            ValueError, match=re.escape("Expected fully qualified feature identifier, received 'Hello, World!'.")
        ):
            FeatureIdentifier("Hello, World!")

    @pytest.mark.parametrize(("string",), INVALID_TEST_CASES)
    async def test_should_raise_for_invalid_identifier_parts(self, string: str):
        with pytest.raises(ValueError, match=rf"Expected fully qualified feature identifier, received '{string}'\."):
            FeatureIdentifier(FeatureIdentifier(string))


class TestCreate:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    async def test_should_create_identifier_from_values(
        self, string: str, originator: str, category: str, feature: str, version: int
    ):
        identifier = FeatureIdentifier.create(originator, category, feature, version)

        assert identifier == string
        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.feature_identifier == string


class TestEquality:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    def test_should_compare_equality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int
    ):
        assert FeatureIdentifier(string) == FeatureIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    def test_should_compare_inequality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int
    ):
        assert (FeatureIdentifier(string) != FeatureIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    def test_should_compare_equality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int
    ):
        assert FeatureIdentifier(string) == string
        assert string == FeatureIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    def test_should_compare_equality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int
    ):
        assert (FeatureIdentifier(string) == object()) is False
        assert (object() == FeatureIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    def test_should_compare_inequality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int
    ):
        assert FeatureIdentifier(string) != object()
        assert object() != FeatureIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    def test_should_compare_inequality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int
    ):
        assert (FeatureIdentifier(string) != string) is False
        assert (string != FeatureIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    def test_should_ignore_case_comparing_equality(
        self, string: str, originator: str, category: str, feature: str, version: int
    ):
        assert FeatureIdentifier(string) == string.lower()
        assert string.lower() == FeatureIdentifier(string)
        assert FeatureIdentifier(string) == string.upper()
        assert string.upper() == FeatureIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    def test_should_ignore_case_comparing_inequality(
        self, string: str, originator: str, category: str, feature: str, version: int
    ):
        assert (FeatureIdentifier(string) != string.lower()) is False
        assert (string.lower() != FeatureIdentifier(string)) is False
        assert (FeatureIdentifier(string) != string.upper()) is False
        assert (string.upper() != FeatureIdentifier(string)) is False


class TestHash:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    def test_should_ignore_case_hashing(self, string: str, originator: str, category: str, feature: str, version: int):
        assert hash(FeatureIdentifier(string)) == hash(FeatureIdentifier(string))
        assert hash(FeatureIdentifier(string)) == hash(FeatureIdentifier(string).lower())


class TestRepresentation:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version"), TEST_CASES)
    def test_should_represent_values(self, string: str, originator: str, category: str, feature: str, version: int):
        assert repr(FeatureIdentifier(string)) == (
            "FeatureIdentifier("
            f"value='{string}', "
            f"originator='{originator}', "
            f"category='{category}', "
            f"feature='{feature}', "
            f"version={version}"
            ")"
        )
