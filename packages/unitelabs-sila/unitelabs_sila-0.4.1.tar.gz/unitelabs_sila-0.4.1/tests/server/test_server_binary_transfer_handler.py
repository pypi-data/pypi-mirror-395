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
from sila.framework.binary_transfer.get_binary_info_request import GetBinaryInfoRequest
from sila.framework.binary_transfer.get_binary_info_response import GetBinaryInfoResponse
from sila.framework.binary_transfer.upload_chunk_request import UploadChunkRequest
from sila.framework.binary_transfer.upload_chunk_response import UploadChunkResponse
from sila.framework.common.server import Server
from sila.framework.errors.framework_error import InvalidMetadata
from sila.server.binary_transfer_handler import ServerBinaryTransferHandler
from sila.testing.raises import raises


class TestSetBinary:
    async def test_should_get_binary(self):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(
            context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Set binary
        binary_transfer_uuid = await handler.set_binary(b"Hello, World!")

        # Assert that the method returns the correct value
        assert isinstance(binary_transfer_uuid, str)


class TestGetBinary:
    async def test_should_get_binary(self):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(
            context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )
        binary_transfer_uuid = await handler.set_binary(b"Hello, World!")

        # Get binary
        binary = await handler.get_binary(binary_transfer_uuid)

        # Assert that the method returns the correct value
        assert binary == b"Hello, World!"

    async def test_should_raise_on_invalid_binary_transfer_uuid(self):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(
            context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Get binary
        with pytest.raises(
            InvalidBinaryTransferUUID, match=r"Expected 'binary_transfer_uuid' with format UUID, received 'abc'\."
        ):
            await handler.get_binary("abc")

    async def test_should_raise_on_unknown_binary_transfer_uuid(self):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(
            context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Get binary
        with pytest.raises(
            InvalidBinaryTransferUUID,
            match=r"Requested unknown Binary with 'binary_transfer_uuid' of '00000000-0000-0000-0000-000000000000'\.",
        ):
            await handler.get_binary("00000000-0000-0000-0000-000000000000")

    async def test_should_raise_on_incomplete_upload(self):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(
            context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )
        handler._binaries["00000000-0000-0000-0000-000000000000"] = BinaryTransfer.new(1, 1)

        # Get binary
        with pytest.raises(
            ValueError,
            match=(
                r"Requested incomplete Binary with 'binary_transfer_uuid' of '00000000-0000-0000-0000-000000000000'\."
            ),
        ):
            await handler.get_binary("00000000-0000-0000-0000-000000000000")


class TestCreateBinary:
    async def test_should_create_empty_binary(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=0,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )

        # Create binary
        response = await handler._create_binary(
            request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Assert that the method returns the correct value
        assert isinstance(response, CreateBinaryResponse)

        # Get binary
        assert await handler.get_binary(response.binary_transfer_uuid) == b""

    async def test_should_create_binary(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        request = CreateBinaryRequest(
            binary_size=1,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )

        # Create binary
        response = await handler._create_binary(
            request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Assert that the method returns the correct value
        assert isinstance(response, CreateBinaryResponse)

        # Get binary
        with pytest.raises(
            ValueError,
            match=rf"Requested incomplete Binary with 'binary_transfer_uuid' of '{response.binary_transfer_uuid}'\.",
        ):
            await handler.get_binary(response.binary_transfer_uuid)

    async def test_should_create_nested_binary(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=0,
            parameter_identifier="org.silastandard/test/ListDataTypeTest/v1/Command/EchoStructureList/Parameter/StructureList",
        )

        # Create binary
        response = await handler._create_binary(
            request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Assert that the method returns the correct value
        assert isinstance(response, CreateBinaryResponse)

        # Get binary
        assert await handler.get_binary(response.binary_transfer_uuid) == b""

    async def test_should_raise_on_invalid_parameter_identifier(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=0,
            parameter_identifier="Invalid",
        )

        # Create binary
        with raises(
            BinaryUploadFailed,
            match=r"Expected a valid fully qualified parameter identifier, received 'Invalid'\.",
        ) as servicer_context:
            await handler._create_binary(request, context=servicer_context)

    async def test_should_raise_on_unknown_parameter_identifier(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=0,
            parameter_identifier="org.silastandard/core/TestFeature/v1/Command/UnobservableCommand/Parameter/Invalid",
        )

        # Create binary
        with raises(
            BinaryUploadFailed,
            match=(
                r"Expected a known fully qualified parameter identifier, received "
                r"'org.silastandard/core/TestFeature/v1/Command/UnobservableCommand/Parameter/Invalid'\."
            ),
        ) as servicer_context:
            await handler._create_binary(request, context=servicer_context)

    async def test_should_raise_on_non_binary_parameter_identifier(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=0,
            parameter_identifier="org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString/Parameter/Integer",
        )

        # Create binary
        with raises(
            BinaryUploadFailed,
            match=r"Expected a fully qualified parameter identifier containing a 'Binary'\.",
        ) as servicer_context:
            await handler._create_binary(request, context=servicer_context)

    async def test_should_raise_on_invalid_metadata(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        request = CreateBinaryRequest(
            binary_size=1,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString/Parameter/Binary",
        )

        # Create binary
        with raises(
            InvalidMetadata,
            match=r"Missing metadata 'String' in UnobservableCommand 'EchoBinaryAndMetadataString'\.",
        ) as servicer_context:
            await handler._create_binary(request, context=servicer_context)


class TestUploadChunk:
    async def test_should_upload_chunk(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler._create_binary(
            create_binary_request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Upload chunk
        async def request_iterator():
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=0, payload=b""
            )

        response = handler._upload_chunk(
            request_iterator(), context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Assert that the method returns the correct value
        chunk_0 = await response.__anext__()
        assert chunk_0.binary_transfer_uuid == create_binary_response.binary_transfer_uuid

        with pytest.raises(StopAsyncIteration):
            await response.__anext__()

        # Get binary
        assert await handler.get_binary(create_binary_response.binary_transfer_uuid) == b""

    async def test_should_upload_multiple_chunks(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=2,
            chunk_count=2,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler._create_binary(
            create_binary_request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Upload chunk
        async def request_iterator():
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=0, payload=b"a"
            )
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=1, payload=b"b"
            )

        response = handler._upload_chunk(
            request_iterator(), context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Assert that the method returns the correct value
        chunk_0 = await response.__anext__()
        assert isinstance(chunk_0, UploadChunkResponse)
        assert chunk_0.binary_transfer_uuid == create_binary_response.binary_transfer_uuid
        assert chunk_0.chunk_index == 0

        chunk_1 = await response.__anext__()
        assert isinstance(chunk_1, UploadChunkResponse)
        assert chunk_1.binary_transfer_uuid == create_binary_response.binary_transfer_uuid
        assert chunk_1.chunk_index == 1

        with pytest.raises(StopAsyncIteration):
            await response.__anext__()

        # Get binary
        assert await handler.get_binary(create_binary_response.binary_transfer_uuid) == b"ab"

    async def test_should_upload_unordered_chunks(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=3,
            chunk_count=3,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler._create_binary(
            create_binary_request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Upload chunk
        async def request_iterator():
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=2, payload=b"c"
            )
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=1, payload=b"b"
            )
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=0, payload=b"a"
            )

        response = handler._upload_chunk(
            request_iterator(), context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Assert that the method returns the correct value
        chunk_0 = await response.__anext__()
        assert isinstance(chunk_0, UploadChunkResponse)
        assert chunk_0.binary_transfer_uuid == create_binary_response.binary_transfer_uuid
        assert chunk_0.chunk_index == 2

        chunk_1 = await response.__anext__()
        assert isinstance(chunk_1, UploadChunkResponse)
        assert chunk_1.binary_transfer_uuid == create_binary_response.binary_transfer_uuid
        assert chunk_1.chunk_index == 1

        chunk_2 = await response.__anext__()
        assert isinstance(chunk_2, UploadChunkResponse)
        assert chunk_2.binary_transfer_uuid == create_binary_response.binary_transfer_uuid
        assert chunk_2.chunk_index == 0

        with pytest.raises(StopAsyncIteration):
            await response.__anext__()

        # Get binary
        assert await handler.get_binary(create_binary_response.binary_transfer_uuid) == b"abc"

    async def test_should_raise_on_invalid_binary_transfer_uuid(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Upload chunk
        async def request_iterator():
            yield UploadChunkRequest(binary_transfer_uuid="Invalid", chunk_index=0, payload=b"")

        with raises(
            InvalidBinaryTransferUUID,
            match=r"Expected 'binary_transfer_uuid' with format UUID, received 'Invalid'\.",
        ) as servicer_context:
            response = handler._upload_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()

    async def test_should_raise_on_unknown_binary_transfer_uuid(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Upload chunk
        async def request_iterator():
            yield UploadChunkRequest(
                binary_transfer_uuid="00000000-0000-0000-0000-000000000000", chunk_index=0, payload=b""
            )

        with raises(
            InvalidBinaryTransferUUID,
            match=r"Requested unknown Binary with 'binary_transfer_uuid' of '00000000-0000-0000-0000-000000000000'\.",
        ) as servicer_context:
            response = handler._upload_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()

    async def test_should_raise_on_expired_binary_transfer_uuid(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Create binary
        binary = BinaryTransfer.new(size=0, chunks=1)
        binary.valid_for = 0.1
        handler._binaries[binary.binary_transfer_uuid] = binary

        await asyncio.sleep(binary.lifetime.total_seconds)

        # Upload chunk
        async def request_iterator():
            yield UploadChunkRequest(binary_transfer_uuid=binary.binary_transfer_uuid, chunk_index=0, payload=b"")

        with raises(
            InvalidBinaryTransferUUID,
            match=rf"Requested Binary '{binary.binary_transfer_uuid}' with exceeded lifetime\.",
        ) as servicer_context:
            response = handler._upload_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()

    async def test_should_raise_on_already_completed_binary(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=0,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler._create_binary(
            create_binary_request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Upload chunk
        async def request_iterator():
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid, chunk_index=0, payload=b""
            )

        with raises(
            BinaryUploadFailed,
            match=r"Received chunk with index '0' for already completed binary transfer\.",
        ) as servicer_context:
            response = handler._upload_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()

    async def test_should_raise_on_oversized_chunk(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler._create_binary(
            create_binary_request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Upload chunk
        async def request_iterator():
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                payload=b" ",
            )

        with (
            unittest.mock.patch("sila.framework.binary_transfer.binary_transfer.BinaryTransfer.max_chunk_size", 0),
            raises(
                BinaryUploadFailed,
                match=r"Expected chunk '0' to not exceed the maximum size of 2 MiB, received 1 bytes\.",
            ) as servicer_context,
        ):
            response = handler._upload_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()

    async def test_should_raise_on_invalid_index(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler._create_binary(
            create_binary_request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Upload chunk
        async def request_iterator():
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=1,
                payload=b"",
            )

        with raises(
            BinaryUploadFailed,
            match=r"Expected chunks up to index '0', received '1'\.",
        ) as servicer_context:
            response = handler._upload_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()

    async def test_should_raise_on_duplicate_chunk(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=1,
            chunk_count=2,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler._create_binary(
            create_binary_request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Upload chunk
        async def request_iterator():
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                payload=b"",
            )
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                payload=b"",
            )

        with raises(
            BinaryUploadFailed,
            match=r"Received chunk with index '0' for already received chunk\.",
        ) as servicer_context:
            response = handler._upload_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()
            await response.__anext__()

    async def test_should_raise_on_overflowing_bytes(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Create binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler._create_binary(
            create_binary_request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Upload chunk
        async def request_iterator():
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                payload=b"...",
            )

        with raises(
            BinaryUploadFailed,
            match=r"Expected a total size of 0 bytes, received already 3 bytes with chunk '0'\.",
        ) as servicer_context:
            response = handler._upload_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()


class TestGetBinaryInfo:
    async def test_should_get_binary_info(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        binary_transfer_uuid = await handler.set_binary(b"Hello, World!")

        # Get binary info
        request = GetBinaryInfoRequest(binary_transfer_uuid=binary_transfer_uuid)
        response = await handler._get_binary_info(
            request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Assert that the method returns the correct value
        assert isinstance(response, GetBinaryInfoResponse)
        assert response.binary_size == 13

    async def test_should_raise_on_invalid_binary_transfer_uuid(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Get binary info
        request = GetBinaryInfoRequest(binary_transfer_uuid="Invalid")

        with raises(
            InvalidBinaryTransferUUID,
            match=r"Expected 'binary_transfer_uuid' with format UUID, received 'Invalid'\.",
        ) as servicer_context:
            await handler._get_binary_info(request, context=servicer_context)

    async def test_should_raise_on_unknown_binary_transfer_uuid(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Get binary info
        request = GetBinaryInfoRequest(binary_transfer_uuid="00000000-0000-0000-0000-000000000000")

        with raises(
            InvalidBinaryTransferUUID,
            match=r"Requested unknown Binary with 'binary_transfer_uuid' of '00000000-0000-0000-0000-000000000000'\.",
        ) as servicer_context:
            await handler._get_binary_info(request, context=servicer_context)

    async def test_should_raise_on_expired_binary_transfer_uuid(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Create binary
        binary = BinaryTransfer.from_buffer(b"Hello, World!")
        binary.valid_for = 0.1
        handler._binaries[binary.binary_transfer_uuid] = binary

        await asyncio.sleep(binary.lifetime.total_seconds)

        # Get binary info
        request = GetBinaryInfoRequest(binary_transfer_uuid=binary.binary_transfer_uuid)
        with raises(
            InvalidBinaryTransferUUID,
            match=rf"Requested Binary '{binary.binary_transfer_uuid}' with exceeded lifetime\.",
        ) as servicer_context:
            await handler._get_binary_info(request, context=servicer_context)


class TestDownloadChunk:
    async def test_should_download_chunk(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        binary_transfer_uuid = await handler.set_binary(b"")

        # Download chunk
        async def request_iterator():
            yield DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=0, length=0)

        response = handler._download_chunk(
            request_iterator(), context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Assert that the method returns the correct value
        chunk_0 = await response.__anext__()
        assert chunk_0.binary_transfer_uuid == binary_transfer_uuid
        assert chunk_0.offset == 0
        assert chunk_0.payload == b""

        with pytest.raises(StopAsyncIteration):
            await response.__anext__()

    async def test_should_download_multiple_chunks(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        binary_transfer_uuid = await handler.set_binary(b"ab")

        # Download chunk
        async def request_iterator():
            yield DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=0, length=1)
            yield DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=1, length=1)

        response = handler._download_chunk(
            request_iterator(), context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Assert that the method returns the correct value
        chunk_0 = await response.__anext__()
        assert chunk_0.binary_transfer_uuid == binary_transfer_uuid
        assert chunk_0.offset == 0
        assert chunk_0.payload == b"a"

        chunk_1 = await response.__anext__()
        assert chunk_1.binary_transfer_uuid == binary_transfer_uuid
        assert chunk_1.offset == 1
        assert chunk_1.payload == b"b"

        with pytest.raises(StopAsyncIteration):
            await response.__anext__()

    async def test_should_download_unordered_chunks(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        binary_transfer_uuid = await handler.set_binary(b"ab")

        # Download chunk
        async def request_iterator():
            yield DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=1, length=1)
            yield DownloadChunkRequest(binary_transfer_uuid=binary_transfer_uuid, offset=0, length=1)

        response = handler._download_chunk(
            request_iterator(), context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Assert that the method returns the correct value
        chunk_0 = await response.__anext__()
        assert chunk_0.binary_transfer_uuid == binary_transfer_uuid
        assert chunk_0.offset == 1
        assert chunk_0.payload == b"b"

        chunk_1 = await response.__anext__()
        assert chunk_1.binary_transfer_uuid == binary_transfer_uuid
        assert chunk_1.offset == 0
        assert chunk_1.payload == b"a"

        with pytest.raises(StopAsyncIteration):
            await response.__anext__()

    async def test_should_raise_on_invalid_binary_transfer_uuid(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Download chunk
        async def request_iterator():
            yield DownloadChunkRequest(binary_transfer_uuid="Invalid", offset=0, length=0)

        with raises(
            InvalidBinaryTransferUUID,
            match=r"Expected 'binary_transfer_uuid' with format UUID, received 'Invalid'\.",
        ) as servicer_context:
            response = handler._download_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()

    async def test_should_raise_on_unknown_binary_transfer_uuid(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Download chunk
        async def request_iterator():
            yield DownloadChunkRequest(binary_transfer_uuid="00000000-0000-0000-0000-000000000000", offset=0, length=0)

        with raises(
            InvalidBinaryTransferUUID,
            match=r"Requested unknown Binary with 'binary_transfer_uuid' of '00000000-0000-0000-0000-000000000000'\.",
        ) as servicer_context:
            response = handler._download_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()

    async def test_should_raise_on_expired_binary_transfer_uuid(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Create binary
        binary = BinaryTransfer.from_buffer(b"Hello, World!")
        binary.valid_for = 0.1
        handler._binaries[binary.binary_transfer_uuid] = binary

        await asyncio.sleep(binary.lifetime.total_seconds)

        # Download chunk
        async def request_iterator():
            yield DownloadChunkRequest(binary_transfer_uuid=binary.binary_transfer_uuid, offset=0, length=0)

        with raises(
            InvalidBinaryTransferUUID,
            match=rf"Requested Binary '{binary.binary_transfer_uuid}' with exceeded lifetime\.",
        ) as servicer_context:
            response = handler._download_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()
            await response.__anext__()

    async def test_should_raise_on_oversized_chunk(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        binary_transfer_uuid = await handler.set_binary(b"ab")

        # Download chunk
        async def request_iterator():
            yield DownloadChunkRequest(
                binary_transfer_uuid=binary_transfer_uuid,
                offset=0,
                length=1,
            )

        with (
            unittest.mock.patch("sila.framework.binary_transfer.binary_transfer.BinaryTransfer.max_chunk_size", 0),
            raises(
                BinaryDownloadFailed,
                match=(
                    r"Expected length of chunk with offset '0' to not exceed the maximum size of 2 MiB, "
                    r"received 1 bytes\."
                ),
            ) as servicer_context,
        ):
            response = handler._download_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()

    async def test_should_raise_on_overflowing_offset(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        binary_transfer_uuid = await handler.set_binary(b"ab")

        # Download chunk
        async def request_iterator():
            yield DownloadChunkRequest(
                binary_transfer_uuid=binary_transfer_uuid,
                offset=3,
                length=1,
            )

        with raises(
            BinaryDownloadFailed,
            match=r"Expected offset to not exceed the binary's size of 2 bytes, received 3 bytes\.",
        ) as servicer_context:
            response = handler._download_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()

    async def test_should_raise_on_overflowing_length(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        binary_transfer_uuid = await handler.set_binary(b"ab")

        # Download chunk
        async def request_iterator():
            yield DownloadChunkRequest(
                binary_transfer_uuid=binary_transfer_uuid,
                offset=1,
                length=2,
            )

        with raises(
            BinaryDownloadFailed,
            match=(
                r"Expected length of chunk with offset '1' to not exceed the binary's size of 2 bytes, "
                r"received 2 bytes\."
            ),
        ) as servicer_context:
            response = handler._download_chunk(request_iterator(), context=servicer_context)
            await response.__anext__()


class TestDeleteBinary:
    async def test_should_delete_binary(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        binary_transfer_uuid = await handler.set_binary(b"Hello, World")

        # Delete binary
        response = await handler._delete_binary(
            DeleteBinaryRequest(binary_transfer_uuid=binary_transfer_uuid),
            context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[])),
        )

        # Assert that the method returns the correct value
        assert isinstance(response, DeleteBinaryResponse)

    async def test_should_delete_uploaded_binary(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        binary_transfer_uuid = await handler.set_binary(b"")

        # Create and upload binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=1,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler._create_binary(
            create_binary_request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        async def request_iterator():
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                payload=b"",
            )

        handler._upload_chunk(
            request_iterator(), context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Delete binary
        response = await handler._delete_binary(
            DeleteBinaryRequest(binary_transfer_uuid=binary_transfer_uuid),
            context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[])),
        )

        # Assert that the method returns the correct value
        assert isinstance(response, DeleteBinaryResponse)

    async def test_should_delete_incomplete_binary(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)
        binary_transfer_uuid = await handler.set_binary(b"")

        # Create and upload binary
        create_binary_request = CreateBinaryRequest(
            binary_size=0,
            chunk_count=2,
            parameter_identifier="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
        )
        create_binary_response = await handler._create_binary(
            create_binary_request, context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        async def request_iterator():
            yield UploadChunkRequest(
                binary_transfer_uuid=create_binary_response.binary_transfer_uuid,
                chunk_index=0,
                payload=b"",
            )

        handler._upload_chunk(
            request_iterator(), context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[]))
        )

        # Delete binary
        response = await handler._delete_binary(
            DeleteBinaryRequest(binary_transfer_uuid=binary_transfer_uuid),
            context=unittest.mock.Mock(invocation_metadata=unittest.mock.Mock(return_value=[])),
        )

        # Assert that the method returns the correct value
        assert isinstance(response, DeleteBinaryResponse)

    async def test_should_raise_on_invalid_binary_transfer_uuid(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Delete binary
        request = DeleteBinaryRequest(binary_transfer_uuid="Invalid")
        with raises(
            InvalidBinaryTransferUUID,
            match=r"Expected 'binary_transfer_uuid' with format UUID, received 'Invalid'\.",
        ) as servicer_context:
            await handler._delete_binary(request, context=servicer_context)

    async def test_should_raise_on_unknown_binary_transfer_uuid(self, server: Server):
        # Create binary transfer handler
        handler = ServerBinaryTransferHandler(server)

        # Delete binary
        request = DeleteBinaryRequest(binary_transfer_uuid="00000000-0000-0000-0000-000000000000")
        with raises(
            InvalidBinaryTransferUUID,
            match=r"Requested unknown Binary with 'binary_transfer_uuid' of '00000000-0000-0000-0000-000000000000'\.",
        ) as servicer_context:
            await handler._delete_binary(request, context=servicer_context)
