import unittest.mock

import grpc

from sila.framework.grpc.create_server import create_server


class TestCreateServer:
    async def test_should_create_secure_server(self):
        server = unittest.mock.Mock(spec=grpc.Server)
        server.add_secure_port = unittest.mock.Mock(return_value=1234)
        credentials = unittest.mock.Mock(spec=grpc.ServerCredentials)

        # Create channel
        with (
            unittest.mock.patch("grpc.aio.server", return_value=server),
            unittest.mock.patch("grpc.ssl_server_credentials", return_value=credentials) as ssl_channel_credentials,
        ):
            response, port = await create_server(unittest.mock.sentinel.address)

        # Assert that the method returns the correct value
        assert response == server
        assert port == 1234
        ssl_channel_credentials.assert_called_once_with(
            private_key_certificate_chain_pairs=[], root_certificates=None, require_client_auth=False
        )
        server.add_secure_port.assert_called_once_with(unittest.mock.sentinel.address, credentials)

    async def test_should_create_insecure_server(self):
        server = unittest.mock.Mock(spec=grpc.Server)
        server.add_insecure_port = unittest.mock.Mock(return_value=1234)

        # Create channel
        with unittest.mock.patch("grpc.aio.server", return_value=server):
            response, port = await create_server(unittest.mock.sentinel.address, tls=False)

        # Assert that the method returns the correct value
        assert response == server
        assert port == 1234
        server.add_insecure_port.assert_called_once_with(unittest.mock.sentinel.address)
