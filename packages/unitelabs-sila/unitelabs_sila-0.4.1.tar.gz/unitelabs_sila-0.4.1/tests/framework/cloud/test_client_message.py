import pytest

from sila.framework.binary_transfer.delete_binary_request import DeleteBinaryRequest
from sila.framework.binary_transfer.download_chunk_request import DownloadChunkRequest
from sila.framework.binary_transfer.get_binary_info_request import GetBinaryInfoRequest
from sila.framework.binary_transfer.upload_chunk_request import UploadChunkRequest
from sila.framework.cloud.cancel_request import CancelRequest
from sila.framework.cloud.client_message import ClientMessage
from sila.framework.cloud.command_execution_request import CommandExecutionRequest
from sila.framework.cloud.command_response_request import CommandResponseRequest
from sila.framework.cloud.create_binary_upload_request import CreateBinaryUploadRequest
from sila.framework.cloud.metadata_request import MetadataRequest
from sila.framework.cloud.property_request import PropertyRequest

ENCODE_TEST_CASES = [
    pytest.param(
        ClientMessage(request_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\x2400000000-0000-0000-0000-000000000000",
        id='1: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            unobservable_command_execution=CommandExecutionRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x12\x02\x12\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 2: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            observable_command_initiation=CommandExecutionRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x1a\x02\x12\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 3: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            observable_command_execution_info=CommandResponseRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x22\x02\x0a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 4: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            observable_command_intermediate_response=CommandResponseRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x2a\x02\x0a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 5: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            observable_command_response=CommandResponseRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x32\x02\x0a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 6: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            metadata_request=MetadataRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x3a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 7: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            unobservable_property_read=PropertyRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x42\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 8: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            observable_property_subscription=PropertyRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x4a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 9: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            cancel_observable_command_execution_info=CancelRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x52\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 10: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            cancel_observable_command_intermediate_response=CancelRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x5a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 11: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            cancel_observable_property=CancelRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x62\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 12: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            create_binary_upload_request=CreateBinaryUploadRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x6a\x02\x12\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 13: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            delete_uploaded_binary_request=DeleteBinaryRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x72\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 14: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            upload_chunk_request=UploadChunkRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x7a\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 15: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            get_binary_info_request=GetBinaryInfoRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x82\x01\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 16: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            download_chunk_request=DownloadChunkRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x8a\x01\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 17: {}',
    ),
    pytest.param(
        ClientMessage(
            request_uuid="00000000-0000-0000-0000-000000000000",
            delete_downloaded_binary_request=DeleteBinaryRequest(),
        ),
        b"\x0a\x2400000000-0000-0000-0000-000000000000\x92\x01\x00",
        id='1: {"00000000-0000-0000-0000-000000000000"}, 18: {}',
    ),
]

DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(
        ClientMessage(request_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x98\x01\x00\x0a\x2400000000-0000-0000-0000-000000000000",
        id='19: 0, 1: {"00000000-0000-0000-0000-000000000000"}',
    ),
]


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode message
        message = ClientMessage.decode(b"")

        # Assert that the method returns the correct value
        assert message == ClientMessage(request_uuid="")

    @pytest.mark.parametrize(("instance", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, instance: ClientMessage, buffer: bytes):
        # Decode message
        message = ClientMessage.decode(buffer)

        # Assert that the method returns the correct value
        assert message == instance

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = ClientMessage.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == ClientMessage(request_uuid="World")

    async def test_should_decode_limited_buffer(self):
        # Decode message
        message = ClientMessage.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == ClientMessage(request_uuid="Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode message
        client_message = ClientMessage()
        message = client_message.encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x24" + client_message.request_uuid.encode()

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
        instance = ClientMessage(request_uuid="00000000-0000-0000-0000-000000000000")
        message = instance.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer
