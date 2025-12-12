import re
import unittest.mock

import grpc
import grpc.aio
import pytest

from sila.framework.errors.connection_error import SiLAConnectionError
from sila.framework.errors.defined_execution_error import DefinedExecutionError
from sila.framework.errors.framework_error import FrameworkError
from sila.framework.errors.sila_error import SiLAError
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila.framework.errors.validation_error import ValidationError
from sila.framework.protobuf.decode_error import DecodeError
from sila.framework.protobuf.encode_error import EncodeError

ENCODE_TEST_CASES = [
    pytest.param(
        ValidationError("Message", "Parameter"),
        b"\x0a\x14\x0a\x09Parameter\x12\x07Message",
        id='1: { 1: {"Parameter"}, 2: {"Message"} }',
    ),
    pytest.param(
        DefinedExecutionError.create("MyError", "My Error")("Message").with_feature(
            "org.silastandard/core/SiLAService/v1"
        ),
        b"\x12\x4d\x0a\x42org.silastandard/core/SiLAService/v1/DefinedExecutionError/MyError\x12\x07Message",
        id='2: { 1: {"org.silastandard/core/SiLAService/v1/DefinedExecutionError/MyError"}, 2: {"Message"} }',
    ),
    pytest.param(UndefinedExecutionError("Message"), b"\x1a\x09\x0a\x07Message", id='3: { 1: {"Message"} }'),
    pytest.param(
        FrameworkError("Message", FrameworkError.Type.NO_METADATA_ALLOWED),
        b"\x22\x0b\x08\x04\x12\x07Message",
        id='4: { 1: 4, 2: {"Message"} }',
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        ValidationError("Message", "Parameter"),
        b"\x0a\x16\x18\x00\x12\x07Message\x0a\x09Parameter",
        id='1: { 3: 0, 2: {"Message"}, 1: {"Parameter"} }',
    ),
    pytest.param(
        ValidationError("Message", "Parameter"),
        b"\x28\x00\x0a\x14\x0a\x09Parameter\x12\x07Message",
        id='5: 0, 1: { 1: {"Parameter"}, 2: {"Message"} }',
    ),
    pytest.param(
        DefinedExecutionError.create("ErrorIdentifier", "Error Identifier")("Message"),
        b"\x12\x1c\x0a\x0fErrorIdentifier\x18\x00\x12\x07Message",
        id='2: { 1: "ErrorIdentifier", 3: 0, 2: {"Message"} }',
    ),
    pytest.param(
        DefinedExecutionError.create("ErrorIdentifier", "Error Identifier")("Message"),
        b"\x12\x1a\x0a\x0fErrorIdentifier\x12\x07Message\x28\x00",
        id='2: { 1: "ErrorIdentifier", 2: {"Message"} }, 5: 0',
    ),
    pytest.param(
        UndefinedExecutionError("Message"), b"\x1a\x0b\x18\x00\x0a\x07Message", id='3: { 3: 0, 1: {"Message"} }'
    ),
    pytest.param(
        UndefinedExecutionError("Message"), b"\x28\x00\x1a\x09\x0a\x07Message", id='5: 0, 3: { 1: {"Message"} }'
    ),
    pytest.param(
        FrameworkError("Message", FrameworkError.Type.INVALID_METADATA),
        b"\x22\x0d\x08\x03\x12\x07Message\x18\x00",
        id='4: { 1: 4, 2: {"Message"}, 3: 0 }',
    ),
    pytest.param(
        FrameworkError("Message", FrameworkError.Type.NO_METADATA_ALLOWED),
        b"\x22\x0b\x08\x04\x12\x07Message\x28\x00",
        id='4: { 1: 4, 2: {"Message"} }, 5: 0',
    ),
]


class TestInitialize:
    async def test_should_initialize(self):
        # Create error
        error = SiLAError("SiLA Error.")

        # Assert that the method returns the correct value
        assert error.message == "SiLA Error."


class TestDecode:
    async def test_should_raise_on_empty_buffer(self):
        # Decode error
        with pytest.raises(DecodeError, match=re.escape("Expected at least one valid error type.")):
            SiLAError.decode(b"")

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: UndefinedExecutionError, buffer: bytes):
        # Decode error
        message = SiLAError.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_limited_buffer(self):
        # Decode error
        message = SiLAError.decode(
            b"\x1a\x03\x0a\x01a\x1a\x03\x0a\x01b",
            len(b"\x1a\x03\x0a\x01a"),
        )

        # Assert that the method returns the correct value
        assert message == UndefinedExecutionError("a")


class TestEncode:
    async def test_should_raise_on_default_values(self):
        # Encode error
        with pytest.raises(EncodeError, match=re.escape("Can only encode subclasses of SiLA error.")):
            SiLAError("").encode()

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: SiLAError, buffer: bytes):
        # Encode error
        message = instance.encode()

        # Assert that the method returns the correct value
        assert message == buffer


class TestToRpcError:
    async def test_should_raise_rpc_error(self):
        # Create context
        abort = unittest.mock.AsyncMock()
        context = unittest.mock.Mock(spec=grpc.aio.ServicerContext, abort=abort)
        error = UndefinedExecutionError("Message")

        # Raise rpc error
        await error.to_rpc_error(context)

        # Assert that the method returns the correct value
        abort.assert_awaited_once_with(code=grpc.StatusCode.ABORTED, details="GgkKB01lc3NhZ2U=")


class TestFromRpcError:
    async def test_should_raise_connection_error(self):
        # Create context
        rpc_error = type(
            "Error",
            (grpc.RpcError,),
            {
                "code": lambda self: grpc.StatusCode.CANCELLED,
                "details": lambda self: "The operation was cancelled (typically by the caller)",
            },
        )()

        # Raise rpc error
        error = await SiLAError.from_rpc_error(rpc_error)

        # Assert that the method returns the correct value
        assert error == SiLAConnectionError("CANCELLED: The operation was cancelled (typically by the caller)")

    async def test_should_raise_execution_error(self):
        # Create context
        rpc_error = type(
            "Error",
            (grpc.RpcError,),
            {
                "code": lambda self: grpc.StatusCode.ABORTED,
                "details": lambda self: "GgkKB01lc3NhZ2U=",
            },
        )()

        # Raise rpc error
        error = await SiLAError.from_rpc_error(rpc_error)

        # Assert that the method returns the correct value
        assert error == UndefinedExecutionError("Message")


class TestEquality:
    def test_should_be_true_on_equal_type(self):
        # Create error
        error_0 = SiLAError("Message")
        error_1 = UndefinedExecutionError("Message")

        # Compare equality
        assert error_0 == error_1

    def test_should_be_false_on_unequal_type(self):
        # Create error
        error_0 = DefinedExecutionError("Message")
        error_1 = UndefinedExecutionError("Message")

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_unequal_message(self):
        # Create error
        error_0 = SiLAError("Message 1")
        error_1 = SiLAError("Message 2")

        # Compare equality
        assert error_0 != error_1

    def test_should_be_false_on_non_sila_error(self):
        # Create error
        error = SiLAError("Defined Execution Error.")

        # Compare equality
        assert error != Exception()
