import unittest.mock

from sila.framework.cloud.client_message import ClientMessage
from sila.framework.cloud.metadata_request import MetadataRequest
from sila.framework.cloud.metadata_response import MetadataResponse
from sila.framework.cloud.server_message import ServerMessage
from sila.server.cloud_server import CloudServer


class TestMetadataRequest:
    async def test_should_request_metadata(self, cloud_server: CloudServer):
        # Read unobservable property
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            metadata_request=MetadataRequest(
                fully_qualified_metadata_id="org.silastandard/test/BinaryTransferTest/v1/Metadata/String"
            ),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            get_fcp_affected_by_metadata_response=MetadataResponse(
                affected_calls=["org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString"]
            ),
        )

    async def test_should_respond_on_unknown_identifier(self, cloud_server: CloudServer):
        # Read unobservable property
        request = ClientMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            metadata_request=MetadataRequest(fully_qualified_metadata_id=""),
        )
        await cloud_server.receive(request)

        # Assert that the method returns the correct value
        response = await cloud_server._responses.__anext__()
        assert response == ServerMessage(
            request_uuid=unittest.mock.sentinel.request_uuid,
            get_fcp_affected_by_metadata_response=MetadataResponse(affected_calls=[]),
        )
