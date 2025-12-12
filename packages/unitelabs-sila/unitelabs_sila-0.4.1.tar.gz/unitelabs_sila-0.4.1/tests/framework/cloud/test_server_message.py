import pytest

from sila.framework.binary_transfer.binary_transfer_error import BinaryTransferError
from sila.framework.binary_transfer.create_binary_response import CreateBinaryResponse
from sila.framework.binary_transfer.delete_binary_response import DeleteBinaryResponse
from sila.framework.binary_transfer.download_chunk_response import DownloadChunkResponse
from sila.framework.binary_transfer.get_binary_info_response import GetBinaryInfoResponse
from sila.framework.binary_transfer.upload_chunk_response import UploadChunkResponse
from sila.framework.cloud.command_confirmation_response import CommandConfirmationResponse
from sila.framework.cloud.command_execution_request import CommandExecutionRequest
from sila.framework.cloud.command_execution_response import CommandExecutionResponse
from sila.framework.cloud.metadata_response import MetadataResponse
from sila.framework.cloud.observable_command_response import ObservableCommandResponse
from sila.framework.cloud.property_response import PropertyResponse
from sila.framework.cloud.server_message import ServerMessage
from sila.framework.cloud.unobservable_command_response import UnobservableCommandResponse
from sila.framework.errors.undefined_execution_error import UndefinedExecutionError

ENCODE_TEST_CASES = [
    pytest.param(
        ServerMessage(request_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\x2400000000-0000-0000-0000-000000000000",
        id='1: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            unobservable_command_response=UnobservableCommandResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x12\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 2: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            observable_command_confirmation=CommandConfirmationResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x1a\x04\x0a\x02\x0a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 3: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            observable_command_execution_info=CommandExecutionResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x22\x04\x0a\x00\x12\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 4: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            observable_command_intermediate_response=ObservableCommandResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x2a\x02\x0a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 5: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            observable_command_response=ObservableCommandResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x32\x02\x0a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 6: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            get_fcp_affected_by_metadata_response=MetadataResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x3a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 7: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            unobservable_property_value=PropertyResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x42\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 8: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            observable_property_value=PropertyResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x4a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 9: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            create_binary_response=CreateBinaryResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x52\x02\x12\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 10: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            upload_chunk_response=UploadChunkResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x5a\x02\x1a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 11: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            delete_binary_response=DeleteBinaryResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x62\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 12: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            get_binary_info_response=GetBinaryInfoResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x6a\x02\x12\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 13: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            download_chunk_response=DownloadChunkResponse(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x72\x02\x22\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 14: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            binary_transfer_error=BinaryTransferError("", BinaryTransferError.Type.INVALID_BINARY_TRANSFER_UUID),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x7a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 15: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            command_error=UndefinedExecutionError(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x82\x01\x02\x1a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 16: {}',
    ),
    pytest.param(
        ServerMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            property_error=UndefinedExecutionError(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x8a\x01\x02\x1a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 17: {}',
    ),
]

DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        ServerMessage(request_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x98\x01\x00\x0a\x2400000000-0000-0000-0000-000000000000",
        id='19: 0, 1: {"00000000-0000-0000-0000-000000000000"}',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = ServerMessage.decode(b"")

        # Assert that the method returns the correct value
        assert message == ServerMessage(request_uuid="")

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: ServerMessage, buffer: bytes):
        # Decode message
        message = ServerMessage.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = ServerMessage.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == ServerMessage(request_uuid="World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = ServerMessage.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == ServerMessage(request_uuid="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        server_message = ServerMessage()
        message = server_message.encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x24" + server_message.request_uuid.encode()

    @pytest.mark.parametrize(("instance", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, instance: CommandExecutionRequest, buffer: bytes):
        # Encode message
        message = instance.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x26\x0a\x2400000000-0000-0000-0000-000000000000", id="default"),
            pytest.param(2, b"\x12\x26\x0a\x2400000000-0000-0000-0000-000000000000", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode message
        instance = ServerMessage(request_uuid="00000000-0000-0000-0000-000000000000")
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
