import pytest

from sila.framework.binary_transfer.binary_transfer_error import (
    BinaryDownloadFailed,
    BinaryTransferError,
    BinaryTransferErrorType,
    BinaryUploadFailed,
    InvalidBinaryTransferUUID,
)

ENCODE_TEST_CASES = [
    pytest.param(
        BinaryTransferError("Binary upload failed.", BinaryTransferErrorType.BINARY_UPLOAD_FAILED),
        b"\x08\x01\x12\x15Binary upload failed.",
        id='1: 1, 2: {"Binary upload failed."}',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        BinaryTransferError("Binary upload failed.", BinaryTransferErrorType.BINARY_UPLOAD_FAILED),
        b"\x08\x01\x12\x15Binary upload failed.\x18\x00",
        id='1: 1, 2: {"Binary upload failed."}, 3: 0',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode error
        message = BinaryTransferError.decode(b"")

        # Assert that the method returns the correct value
        assert message == BinaryTransferError("", BinaryTransferErrorType.INVALID_BINARY_TRANSFER_UUID)

    @pytest.mark.parametrize(("error", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, error: BinaryTransferError, buffer: bytes):
        # Decode error
        message = BinaryTransferError.decode(buffer)

        # Assert that the method returns the correct value
        assert message == error

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = BinaryTransferError.decode(b"\x08\x01\x08\x00")

        # Assert that the method returns the correct value
        assert message == BinaryTransferError("", BinaryTransferErrorType.INVALID_BINARY_TRANSFER_UUID)

    async def test_should_decode_limited_buffer(self):
        # Decode error
        message = BinaryTransferError.decode(b"\x08\x01\x08\x00", 2)

        # Assert that the method returns the correct value
        assert message == BinaryTransferError("", BinaryTransferErrorType.BINARY_UPLOAD_FAILED)


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode error
        message = BinaryTransferError("", BinaryTransferErrorType.INVALID_BINARY_TRANSFER_UUID).encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("error", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, error: BinaryTransferError, buffer: bytes):
        # Encode error
        message = error.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x00", id="default"),
            pytest.param(2, b"\x12\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode error
        error = InvalidBinaryTransferUUID("")
        message = error.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestEquality:
    def test_should_be_true_on_equal_type(self):
        # Create error
        error_0 = InvalidBinaryTransferUUID("Unknown UUID.")
        error_1 = InvalidBinaryTransferUUID("Unknown UUID.")

        # Compare equality
        assert error_0 == error_1

    def test_should_be_false_on_unequal_type(self):
        # Create error
        error_0 = InvalidBinaryTransferUUID("Unknown UUID.")
        error_1 = BinaryUploadFailed("Unknown UUID.")

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_unequal_message(self):
        # Create error
        error_0 = InvalidBinaryTransferUUID("Unknown UUID.")
        error_1 = InvalidBinaryTransferUUID("Malformed UUID.")

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_non_sila_error(self):
        # Create error
        error = BinaryDownloadFailed("Unknown UUID.")

        # Compare equality
        assert error != Exception()
