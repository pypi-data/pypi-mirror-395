import grpc
import pytest

from sila.framework.binary_transfer.binary_transfer_error import BinaryTransferError, InvalidBinaryTransferUUID
from sila.framework.errors.sila_error import SiLAError
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila.testing.raises import raises


class TestRaises:
    async def test_should_detect_sila_error(self):
        with raises(SiLAError) as context:
            await UndefinedExecutionError("").to_rpc_error(context)

    async def test_should_match_message(self):
        with raises(BinaryTransferError, match=r"Hello World") as context:
            await InvalidBinaryTransferUUID(message="Hello World!").to_rpc_error(context)

    async def test_should_raise_on_missing_error(self):
        with pytest.raises(AssertionError, match=rf"Did not raise {SiLAError}"), raises(SiLAError):
            pass

    async def test_should_raise_on_invalid_code(self):
        with (
            pytest.raises(AssertionError, match=r"Expected status code to be 'aborted', received 'ok'\."),
            raises(SiLAError) as context,
        ):
            await context.abort(code=grpc.StatusCode.OK)

    async def test_should_raise_on_invalid_message(self):
        with (
            pytest.raises(
                AssertionError, match=r"Regex pattern did not match\.\n Regex: 'Hello, World!'\n Input: 'Hello, me!'"
            ),
            raises(SiLAError, match=r"Hello, World!") as context,
        ):
            await UndefinedExecutionError(message="Hello, me!").to_rpc_error(context)
