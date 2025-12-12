import asyncio
import unittest.mock

import pytest

from sila.framework.binary_transfer.binary_transfer import BinaryTransfer
from sila.framework.binary_transfer.binary_transfer_error import (
    BinaryDownloadFailed,
    BinaryUploadFailed,
    InvalidBinaryTransferUUID,
)
from sila.framework.binary_transfer.create_binary_request import CreateBinaryRequest
from sila.framework.binary_transfer.create_binary_response import CreateBinaryResponse
from sila.framework.binary_transfer.delete_binary_request import DeleteBinaryRequest
from sila.framework.binary_transfer.delete_binary_response import DeleteBinaryResponse
from sila.framework.binary_transfer.download_chunk_request import DownloadChunkRequest
from sila.framework.binary_transfer.download_chunk_response import DownloadChunkResponse
from sila.framework.binary_transfer.get_binary_info_request import GetBinaryInfoRequest
from sila.framework.binary_transfer.get_binary_info_response import GetBinaryInfoResponse
from sila.framework.binary_transfer.upload_chunk_request import UploadChunkRequest
from sila.framework.binary_transfer.upload_chunk_response import UploadChunkResponse
from sila.framework.cloud.client_message import ClientMessage
from sila.framework.cloud.create_binary_upload_request import CreateBinaryUploadRequest
from sila.framework.cloud.server_message import ServerMessage
from sila.framework.errors.framework_error import InvalidMetadata
from sila.server.cloud_server import CloudServer


class TestCreateBinaryUploadRequest:
    async def test_should_create_empty_binary(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=0,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )

        # Create binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            create_binary_upload_request=CreateBinaryUploadRequest(create_binary_request=request),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            create_binary_response=CreateBinaryResponse(
                binary_transfer_uuid=unittest.mock.ANY,
                lifetime_of_binary=unittest.mock.ANY,
            ),
        )
        response = server_message.create_binary_response
        assert response

        # Get binary
        assert await handler.get_binary(response.binary_transfer_uuid) == b""

    async def test_should_create_binary(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        request = CreateBinaryRequest(
            binary_size=1,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )

        # Create binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            create_binary_upload_request=CreateBinaryUploadRequest(create_binary_request=request),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            create_binary_response=CreateBinaryResponse(
                binary_transfer_uuid=unittest.mock.ANY,
                lifetime_of_binary=unittest.mock.ANY,
            ),
        )
        response = server_message.create_binary_response
        assert response

        # Get binary
        with pytest.raises(
            ValueError,
            match=rf"Requested incomplete Binary with 'binary_transfer_uuid' of '{response.binary_transfer_uuid}'\.",
        ):
            await handler.get_binary(response.binary_transfer_uuid)

    async def test_should_raise_on_invalid_parameter_identifier(self, cloud_server: CloudServer):
        # Create binary transfer handler
        request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=0,
            parameter_identifier="Invalid",
        )

        # Create binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            create_binary_upload_request=CreateBinaryUploadRequest(create_binary_request=request),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=BinaryUploadFailed(
                "Expected a valid fully qualified parameter identifier, received 'Invalid'."
            ),
        )

    async def test_should_raise_on_unknown_parameter_identifier(self, cloud_server: CloudServer):
        # Create binary transfer handler
        request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=0,
            parameter_identifier="org.silastandard/core/TestFeature/v1/Command/UnobservableCommand/Parameter/Invalid",
        )

        # Create binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            create_binary_upload_request=CreateBinaryUploadRequest(create_binary_request=request),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=BinaryUploadFailed(
                "Expected a known fully qualified parameter identifier, received "
                "'org.silastandard/core/TestFeature/v1/Command/UnobservableCommand/Parameter/Invalid'."
            ),
        )

    async def test_should_raise_on_non_binary_parameter_identifier(self, cloud_server: CloudServer):
        # Create binary transfer handler
        request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=0,
            parameter_identifier="org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString/Parameter/Integer",
        )

        # Create binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            create_binary_upload_request=CreateBinaryUploadRequest(create_binary_request=request),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=BinaryUploadFailed(
                "Expected a fully qualified parameter identifier containing a 'Binary'."
            ),
        )

    async def test_should_raise_on_invalid_metadata(self, cloud_server: CloudServer):
        # Create binary transfer handler
        request = CreateBinaryRequest(
            binary_size=1,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString/Parameter/Binary",
        )

        # Create binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            create_binary_upload_request=CreateBinaryUploadRequest(create_binary_request=request),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            command_error=InvalidMetadata(
                "Missing metadata 'String' in UnobservableCommand 'EchoBinaryAndMetadataString'."
            ),
        )


class TestUploadChunkRequest:
    async def test_should_upload_chunk(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=0, payload=b""
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_response=UploadChunkResponse(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                lifetime_of_binary=unittest.mock.ANY,
            ),
        )

        # Get binary
        assert await handler.get_binary(create_binary_response.binary_transfer_uuid) == b""

    async def test_should_upload_multiple_chunks(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=2,
            chunk_count=2,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=0, payload=b"a"
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_response=UploadChunkResponse(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                lifetime_of_binary=unittest.mock.ANY,
            ),
        )

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=1, payload=b"b"
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_response=UploadChunkResponse(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=1,
                lifetime_of_binary=unittest.mock.ANY,
            ),
        )

        # Get binary
        assert await handler.get_binary(create_binary_response.binary_transfer_uuid) == b"ab"

    async def test_should_upload_unordered_chunks(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=3,
            chunk_count=3,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=2, payload=b"c"
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_response=UploadChunkResponse(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=2,
                lifetime_of_binary=unittest.mock.ANY,
            ),
        )

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=1, payload=b"b"
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_response=UploadChunkResponse(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=1,
                lifetime_of_binary=unittest.mock.ANY,
            ),
        )

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=0, payload=b"a"
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_response=UploadChunkResponse(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                lifetime_of_binary=unittest.mock.ANY,
            ),
        )

        # Get binary
        assert await handler.get_binary(create_binary_response.binary_transfer_uuid) == b"abc"

    async def test_should_raise_on_invalid_binary_transfer_uuid(self, cloud_server: CloudServer):
        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(binary_transfer_uuid="Invalid", chunk_index=0, payload=b""),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=InvalidBinaryTransferUUID(
                "Expected 'binary_transfer_uuid' with format UUID, received 'Invalid'."
            ),
        )

    async def test_should_raise_on_unknown_binary_transfer_uuid(self, cloud_server: CloudServer):
        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid="00000000-0000-0000-0000-000000000000", chunk_index=0, payload=b""
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=InvalidBinaryTransferUUID(
                "Requested unknown Binary with 'binary_transfer_uuid' of '00000000-0000-0000-0000-000000000000'."
            ),
        )

    async def test_should_raise_on_expired_binary_transfer_uuid(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler

        # Create binary
        binary = BinaryTransfer.new(size=0, chunks=1)
        binary.valid_for = 0.1
        handler._binaries[binary.binary_transfer_uuid] = binary

        await asyncio.sleep(binary.lifetime.total_seconds)

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=binary.binary_transfer_uuid, chunk_index=0, payload=b""
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=InvalidBinaryTransferUUID(
                f"Requested Binary '{binary.binary_transfer_uuid}' with exceeded lifetime."
            ),
        )

    async def test_should_raise_on_already_completed_binary(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=0,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=0, payload=b""
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=BinaryUploadFailed(
                "Received chunk with index '0' for already completed binary transfer."
            ),
        )

    async def test_should_raise_on_oversized_chunk(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                payload=b" " * (2**21 + 1),
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=BinaryUploadFailed(
                "Expected chunk '0' to not exceed the maximum size of 2 MiB, received 2097153 bytes."
            ),
        )

    async def test_should_raise_on_invalid_index(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=1,
                payload=b"",
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=BinaryUploadFailed("Expected chunks up to index '0', received '1'."),
        )

    async def test_should_raise_on_duplicate_chunk(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=1,
            chunk_count=2,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                payload=b"",
            ),
        )
        await cloud_server.receive(client_message)
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=BinaryUploadFailed("Received chunk with index '0' for already received chunk."),
        )

    async def test_should_raise_on_overflowing_bytes(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        # Upload chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            upload_chunk_request=UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                payload=b"...",
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=BinaryUploadFailed(
                "Expected a total size of 0 bytes, received already 3 bytes with chunk '0'."
            ),
        )


class TestDeleteUploadedBinary:
    async def test_should_delete_binary(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"Hello, World")

        # Delete binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_uploaded_binary_request=DeleteBinaryRequest(
                binary_transfer_uuid=binary_transfer_uuid,
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_binary_response=DeleteBinaryResponse(),
        )

    async def test_should_delete_uploaded_binary(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"")

        # Create and upload binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        upload_chunk_request = UploadChunkRequest(
            binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
            chunk_index=0,
            payload=b"",
        )
        await handler.upload_chunk(upload_chunk_request)

        # Delete binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_uploaded_binary_request=DeleteBinaryRequest(
                binary_transfer_uuid=binary_transfer_uuid,
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_binary_response=DeleteBinaryResponse(),
        )

    async def test_should_delete_incomplete_binary(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"")

        # Create and upload binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=2,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        upload_chunk_request = UploadChunkRequest(
            binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
            chunk_index=0,
            payload=b"",
        )
        await handler.upload_chunk(upload_chunk_request)

        # Delete binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_uploaded_binary_request=DeleteBinaryRequest(
                binary_transfer_uuid=binary_transfer_uuid,
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_binary_response=DeleteBinaryResponse(),
        )

    async def test_should_raise_on_invalid_binary_transfer_uuid(self, cloud_server: CloudServer):
        # Delete binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_uploaded_binary_request=DeleteBinaryRequest(
                binary_transfer_uuid="Invalid",
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=InvalidBinaryTransferUUID(
                "Expected 'binary_transfer_uuid' with format UUID, received 'Invalid'."
            ),
        )


class TestGetBinaryInfo:
    async def test_should_get_binary_info(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"Hello, World!")

        # Get binary info
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            get_binary_info_request=GetBinaryInfoRequest(binary_transfer_uuid=binary_transfer_uuid),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            get_binary_info_response=GetBinaryInfoResponse(
                binary_size=13,
                lifetime_of_binary=unittest.mock.ANY,
            ),
        )

    async def test_should_raise_on_invalid_binary_transfer_uuid(self, cloud_server: CloudServer):
        # Get binary info
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            get_binary_info_request=GetBinaryInfoRequest(binary_transfer_uuid="Invalid"),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=InvalidBinaryTransferUUID(
                "Expected 'binary_transfer_uuid' with format UUID, received 'Invalid'."
            ),
        )

    async def test_should_raise_on_unknown_binary_transfer_uuid(self, cloud_server: CloudServer):
        # Get binary info
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            get_binary_info_request=GetBinaryInfoRequest(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=InvalidBinaryTransferUUID(
                "Requested unknown Binary with 'binary_transfer_uuid' of '00000000-0000-0000-0000-000000000000'."
            ),
        )

    async def test_should_raise_on_expired_binary_transfer_uuid(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler

        # Create binary
        binary = BinaryTransfer.from_buffer(b"Hello, World!")
        binary.valid_for = 0.1
        handler._binaries[binary.binary_transfer_uuid] = binary

        await asyncio.sleep(binary.lifetime.total_seconds)

        # Get binary info
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            get_binary_info_request=GetBinaryInfoRequest(binary_transfer_uuid=binary.binary_transfer_uuid),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=InvalidBinaryTransferUUID(
                f"Requested Binary '{binary.binary_transfer_uuid}' with exceeded lifetime."
            ),
        )


class TestDownloadChunk:
    async def test_should_download_chunk(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"")

        # Download chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_request=DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=0, length=0),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_response=DownloadChunkResponse(
                binary_transfer_uuid=binary_transfer_uuid, offset=0, payload=b"", lifetime_of_binary=unittest.mock.ANY
            ),
        )

    async def test_should_download_multiple_chunks(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"ab")

        # Download chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_request=DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=0, length=1),
        )
        await cloud_server.receive(client_message)

        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_request=DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=1, length=1),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_response=DownloadChunkResponse(
                binary_transfer_uuid=binary_transfer_uuid, offset=0, payload=b"a", lifetime_of_binary=unittest.mock.ANY
            ),
        )

        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_response=DownloadChunkResponse(
                binary_transfer_uuid=binary_transfer_uuid, offset=1, payload=b"b", lifetime_of_binary=unittest.mock.ANY
            ),
        )

    async def test_should_download_unordered_chunks(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"ab")

        # Download chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_request=DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=1, length=1),
        )
        await cloud_server.receive(client_message)

        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_request=DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=0, length=1),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_response=DownloadChunkResponse(
                binary_transfer_uuid=binary_transfer_uuid, offset=1, payload=b"b", lifetime_of_binary=unittest.mock.ANY
            ),
        )

        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_response=DownloadChunkResponse(
                binary_transfer_uuid=binary_transfer_uuid, offset=0, payload=b"a", lifetime_of_binary=unittest.mock.ANY
            ),
        )

    async def test_should_raise_on_invalid_binary_transfer_uuid(self, cloud_server: CloudServer):
        # Download chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_request=DownloadChunkRequest(binary_transfer_uuid="Invalid", offset=0, length=0),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=InvalidBinaryTransferUUID(
                "Expected 'binary_transfer_uuid' with format UUID, received 'Invalid'."
            ),
        )

    async def test_should_raise_on_unknown_binary_transfer_uuid(self, cloud_server: CloudServer):
        # Download chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_request=DownloadChunkRequest(
                binary_transfer_uuid="00000000-0000-0000-0000-000000000000", offset=0, length=0
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=InvalidBinaryTransferUUID(
                "Requested unknown Binary with 'binary_transfer_uuid' of '00000000-0000-0000-0000-000000000000'."
            ),
        )

    async def test_should_raise_on_expired_binary_transfer_uuid(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler

        # Create binary
        binary = BinaryTransfer.from_buffer(b"Hello, World!")
        binary.valid_for = 0.1
        handler._binaries[binary.binary_transfer_uuid] = binary

        await asyncio.sleep(binary.lifetime.total_seconds)

        # Download chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_request=DownloadChunkRequest(
                binary_transfer_uuid=binary.binary_transfer_uuid, offset=0, length=0
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=InvalidBinaryTransferUUID(
                f"Requested Binary '{binary.binary_transfer_uuid}' with exceeded lifetime."
            ),
        )

    async def test_should_raise_on_oversized_chunk(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"ab")

        # Download chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_request=DownloadChunkRequest(
                binary_transfer_uuid=binary_transfer_uuid, offset=0, length=2**21 + 1
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=BinaryDownloadFailed(
                "Expected length of chunk with offset '0' to not exceed the maximum size of 2 MiB, "
                "received 2097153 bytes."
            ),
        )

    async def test_should_raise_on_overflowing_offset(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"ab")

        # Download chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_request=DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=3, length=1),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=BinaryDownloadFailed(
                "Expected offset to not exceed the binary's size of 2 bytes, received 3 bytes."
            ),
        )

    async def test_should_raise_on_overflowing_length(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"ab")

        # Download chunk
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            download_chunk_request=DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=1, length=2),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=BinaryDownloadFailed(
                "Expected length of chunk with offset '1' to not exceed the binary's size of 2 bytes, received 2 bytes."
            ),
        )


class TestDeleteDownloadedBinary:
    async def test_should_delete_binary(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"Hello, World")

        # Delete binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_downloaded_binary_request=DeleteBinaryRequest(
                binary_transfer_uuid=binary_transfer_uuid,
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_binary_response=DeleteBinaryResponse(),
        )

    async def test_should_delete_uploaded_binary(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"")

        # Create and upload binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        upload_chunk_request = UploadChunkRequest(
            binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
            chunk_index=0,
            payload=b"",
        )
        await handler.upload_chunk(upload_chunk_request)

        # Delete binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_downloaded_binary_request=DeleteBinaryRequest(
                binary_transfer_uuid=binary_transfer_uuid,
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_binary_response=DeleteBinaryResponse(),
        )

    async def test_should_delete_incomplete_binary(self, cloud_server: CloudServer):
        # Create binary transfer handler
        handler = cloud_server._binary_transfer_handler
        binary_transfer_uuid = await handler.set_binary(b"")

        # Create and upload binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=2,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler.create_binary(create_binary_request)

        upload_chunk_request = UploadChunkRequest(
            binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
            chunk_index=0,
            payload=b"",
        )
        await handler.upload_chunk(upload_chunk_request)

        # Delete binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_downloaded_binary_request=DeleteBinaryRequest(
                binary_transfer_uuid=binary_transfer_uuid,
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_binary_response=DeleteBinaryResponse(),
        )

    async def test_should_raise_on_invalid_binary_transfer_uuid(self, cloud_server: CloudServer):
        # Delete binary
        client_message = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            delete_downloaded_binary_request=DeleteBinaryRequest(
                binary_transfer_uuid="Invalid",
            ),
        )
        await cloud_server.receive(client_message)

        # Assert that the method returns the correct value
        server_message = await cloud_server._responses.__anext__()
        assert server_message == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            binary_transfer_error=InvalidBinaryTransferUUID(
                "Expected 'binary_transfer_uuid' with format UUID, received 'Invalid'."
            ),
        )
