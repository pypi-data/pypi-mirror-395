import unittest.mock

import grpc

from sila.framework.grpc.create_channel import create_channel


class TestCreateChannel:
    async def test_should_create_secure_channel(self):
        channel = unittest.mock.Mock(spec=grpc.Channel)
        credentials = unittest.mock.Mock(spec=grpc.ChannelCredentials)

        # Create channel
        with (
            unittest.mock.patch("grpc.aio.secure_channel", return_value=channel) as secure_channel,
            unittest.mock.patch("grpc.ssl_channel_credentials", return_value=credentials) as ssl_channel_credentials,
        ):
            response = await create_channel(unittest.mock.sentinel.address)

        # Assert that the method returns the correct value
        assert response == channel
        ssl_channel_credentials.assert_called_once_with(
            root_certificates=None, private_key=None, certificate_chain=None
        )
        secure_channel.assert_called_once_with(unittest.mock.sentinel.address, credentials=credentials, options=[])

    async def test_should_create_secure_channel_with_certificates(self):
        channel = unittest.mock.Mock(spec=grpc.Channel)
        credentials = unittest.mock.Mock(spec=grpc.ChannelCredentials)

        # Create channel
        with (
            unittest.mock.patch("grpc.aio.secure_channel", return_value=channel) as secure_channel,
            unittest.mock.patch("grpc.ssl_channel_credentials", return_value=credentials) as ssl_channel_credentials,
        ):
            await create_channel(
                unittest.mock.sentinel.address,
                root_certificates=unittest.mock.sentinel.root_certificates,
                private_key=unittest.mock.sentinel.private_key,
                certificate_chain=unittest.mock.sentinel.certificate_chain,
            )

        # Assert that the method returns the correct value
        ssl_channel_credentials.assert_called_once_with(
            root_certificates=unittest.mock.sentinel.root_certificates,
            private_key=unittest.mock.sentinel.private_key,
            certificate_chain=unittest.mock.sentinel.certificate_chain,
        )
        secure_channel.assert_called_once_with(unittest.mock.sentinel.address, credentials=credentials, options=[])

    async def test_should_create_secure_channel_with_options(self):
        channel = unittest.mock.Mock(spec=grpc.Channel)
        credentials = unittest.mock.Mock(spec=grpc.ChannelCredentials)

        # Create channel
        with (
            unittest.mock.patch("grpc.aio.secure_channel", return_value=channel) as secure_channel,
            unittest.mock.patch("grpc.ssl_channel_credentials", return_value=credentials) as ssl_channel_credentials,
        ):
            await create_channel(unittest.mock.sentinel.address, options={"grpc.keepalive_time_ms": 1000})

        # Assert that the method returns the correct value
        ssl_channel_credentials.assert_called_once_with(
            root_certificates=None, private_key=None, certificate_chain=None
        )
        secure_channel.assert_called_once_with(
            unittest.mock.sentinel.address, credentials=credentials, options=[("grpc.keepalive_time_ms", 1000)]
        )

    async def test_should_create_insecure_channel(self):
        channel = unittest.mock.Mock(spec=grpc.Channel)

        # Create channel
        with unittest.mock.patch("grpc.aio.insecure_channel", return_value=channel) as insecure_channel:
            response = await create_channel(unittest.mock.sentinel.address, tls=False)

        # Assert that the method returns the correct value
        assert response == channel
        insecure_channel.assert_called_once_with(unittest.mock.sentinel.address, options=[])

    async def test_should_create_insecure_channel_with_options(self):
        channel = unittest.mock.Mock(spec=grpc.Channel)

        # Create channel
        with unittest.mock.patch("grpc.aio.insecure_channel", return_value=channel) as insecure_channel:
            await create_channel(unittest.mock.sentinel.address, tls=False, options={"grpc.keepalive_time_ms": 1000})

        # Assert that the method returns the correct value
        insecure_channel.assert_called_once_with(
            unittest.mock.sentinel.address, options=[("grpc.keepalive_time_ms", 1000)]
        )
