import pytest

from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.errors.sila_error import SiLAError
from sila.framework.errors.validation_error import ValidationError

ENCODE_TEST_CASES = [
    pytest.param(
        ValidationError(
            "Invalid Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        ),
        (
            b"\x0a\x73\x0a\x5dorg.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"
            b"\x12\x12Invalid Parameter."
        ),
        id=(
            '1: { 1: "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier", '
            '2: "Invalid Parameter." }'
        ),
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        ValidationError(
            "Invalid Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        ),
        (
            b"\x0a\x75\x0a\x5dorg.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"
            b"\x12\x12Invalid Parameter.\x18\x00"
        ),
        id=(
            '1: { 1: "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier", '
            '2: "Invalid Parameter.", 3: 0 }'
        ),
    ),
]


class TestInitialize:
    async def test_should_initialize(self):
        # Create error
        error = ValidationError(
            "Invalid Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        )

        # Assert that the method returns the correct value
        assert error.message == "Invalid Parameter."
        assert (
            error.parameter
            == "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"
        )


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode error
        message = ValidationError.decode(b"")

        # Assert that the method returns the correct value
        assert message == ValidationError("", "")

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: ValidationError, buffer: bytes):
        # Decode error
        message = SiLAError.decode(buffer)

        # Assert that the method returns the correct value
        assert isinstance(message, ValidationError)
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode error
        message = ValidationError.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == ValidationError("", "World")

    async def test_should_decode_limited_buffer(self):
        # Decode error
        message = ValidationError.decode(
            b"\x0a\x05Hello\x0a\x05World",
            len(b"\x0a\x05Hello"),
        )

        # Assert that the method returns the correct value
        assert message == ValidationError("", "Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode error
        message = ValidationError("", "").encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x00"

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: ValidationError, buffer: bytes):
        # Encode error
        message = instance.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x02\x0a\x00", id="default"),
            pytest.param(2, b"\x12\x02\x0a\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode error
        instance = ValidationError("", "")
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestStringify:
    async def test_should_convert_to_string(self):
        # Create error
        error = ValidationError(
            "Invalid Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        )

        # Assert that the method returns the correct value
        assert str(error) == "Invalid Parameter."


class TestEquality:
    def test_should_be_true_on_equal_type(self):
        # Create error
        error_0 = ValidationError(
            "Invalid Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        )
        error_1 = ValidationError(
            "Invalid Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        )

        # Compare equality
        assert error_0 == error_1

    def test_should_be_false_on_unequal_type(self):
        # Create error
        error_0 = ValidationError(
            "Invalid Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        )
        error_1 = DefinedExecutionError("Undefined Execution Error.")

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_unequal_message(self):
        # Create error
        error_0 = ValidationError(
            "Invalid Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        )
        error_1 = ValidationError(
            "Missing Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        )

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_unequal_parameter(self):
        # Create error
        error_0 = ValidationError(
            "Invalid Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        )
        error_1 = ValidationError(
            "Invalid Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/Identifier",
        )

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_non_sila_error(self):
        # Create error
        error = ValidationError(
            "Invalid Parameter.",
            "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
        )

        # Compare equality
        assert error != Exception()
