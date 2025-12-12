# ruff: noqa: A002


import re

import pytest

from sila.framework.identifiers.data_type_identifier import DataTypeIdentifier
from sila.framework.identifiers.feature_identifier import FeatureIdentifier

TEST_CASES = [
    pytest.param(
        "org.silastandard/core/ErrorRecoveryService/v1/DataType/ContinuationOption",
        "org.silastandard",
        "core",
        "ErrorRecoveryService",
        1,
        "ContinuationOption",
        id="org.silastandard/core/ErrorRecoveryService/v1/DataType/ContinuationOption",
    ),
    pytest.param(
        "org.silastandard/test/StructureDataTypeTest/v1/DataType/TestStructure",
        "org.silastandard",
        "test",
        "StructureDataTypeTest",
        1,
        "TestStructure",
        id="org.silastandard/test/StructureDataTypeTest/v1/DataType/TestStructure",
    ),
    pytest.param(
        "org.silastandard/test/ListDataTypeTest/v1/DataType/TestStructure",
        "org.silastandard",
        "test",
        "ListDataTypeTest",
        1,
        "TestStructure",
        id="org.silastandard/test/ListDataTypeTest/v1/DataType/TestStructure",
    ),
]


class TestInitialize:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    async def test_should_init_identifier_from_string(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        identifier = DataTypeIdentifier(string)

        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.data_type == data_type
        assert identifier.feature_identifier == string.rpartition("/DataType/")[0]

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    async def should_infer_identifier_type(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        identifier = FeatureIdentifier(string)

        assert isinstance(identifier, DataTypeIdentifier)
        assert identifier == string

    async def test_should_raise_for_malformed_identifier(self):
        with pytest.raises(
            ValueError, match=re.escape("Expected fully qualified feature identifier, received 'Hello, World!'.")
        ):
            DataTypeIdentifier("Hello, World!")

    async def test_should_raise_for_wrong_identifier(self):
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected fully qualified feature identifier, received 'org.silastandard/core/SiLAService/v1'."
            ),
        ):
            DataTypeIdentifier("org.silastandard/core/SiLAService/v1")


class TestCreate:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    async def test_should_create_identifier_from_values(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        identifier = DataTypeIdentifier.create(originator, category, feature, version, data_type)

        assert identifier == string
        assert identifier.originator == originator
        assert identifier.category == category
        assert identifier.feature == feature
        assert identifier.version == version
        assert identifier.data_type == data_type
        assert identifier.feature_identifier == string.rpartition("/DataType/")[0]


class TestEquality:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    def test_should_compare_equality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        assert DataTypeIdentifier(string) == DataTypeIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    def test_should_compare_inequality_to_identifier(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        assert (DataTypeIdentifier(string) != DataTypeIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    def test_should_compare_equality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        assert DataTypeIdentifier(string) == string
        assert string == DataTypeIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    def test_should_compare_equality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        assert (DataTypeIdentifier(string) == object()) is False
        assert (object() == DataTypeIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    def test_should_compare_inequality_to_non_string(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        assert DataTypeIdentifier(string) != object()
        assert object() != DataTypeIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    def test_should_compare_inequality_to_string(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        assert (DataTypeIdentifier(string) != string) is False
        assert (string != DataTypeIdentifier(string)) is False

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    def test_should_ignore_case_comparing_equality(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        assert DataTypeIdentifier(string) == string.lower()
        assert string.lower() == DataTypeIdentifier(string)
        assert DataTypeIdentifier(string) == string.upper()
        assert string.upper() == DataTypeIdentifier(string)

    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    def test_should_ignore_case_comparing_inequality(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        assert (DataTypeIdentifier(string) != string.lower()) is False
        assert (string.lower() != DataTypeIdentifier(string)) is False
        assert (DataTypeIdentifier(string) != string.upper()) is False
        assert (string.upper() != DataTypeIdentifier(string)) is False


class TestRepresentation:
    @pytest.mark.parametrize(("string", "originator", "category", "feature", "version", "data_type"), TEST_CASES)
    def test_should_represent_values(
        self, string: str, originator: str, category: str, feature: str, version: int, data_type: str
    ):
        assert repr(DataTypeIdentifier(string)) == (
            "DataTypeIdentifier("
            f"value='{string}', "
            f"originator='{originator}', "
            f"category='{category}', "
            f"feature='{feature}', "
            f"version={version}, "
            f"data_type='{data_type}'"
            ")"
        )
