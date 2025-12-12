import asyncio
import dataclasses
import unittest.mock

import grpc.aio
import pytest

from sila.framework.cloud.client_message import ClientMessage
from sila.framework.cloud.server_message import ServerMessage
from sila.framework.grpc.channel_options import ChannelOptions
from sila.framework.protobuf.encode_error import EncodeError
from sila.server.cloud_server import CloudServer, CloudServerConfig
from sila.server.server import Server
from sila.server.sila_service import SiLAService


class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration from None


class TestContext:
    async def test_should_use_self_as_context(self):
        # Create server
        cloud_server = CloudServer()
        sila_service = SiLAService()

        # Register feature
        cloud_server.register_feature(sila_service)

        # Assert that the method returns the correct value
        assert cloud_server.context == cloud_server
        assert cloud_server.get_feature(sila_service.fully_qualified_identifier) == sila_service

    async def test_should_override_context_with_server(self):
        # Create server
        server = Server()
        cloud_server = CloudServer()
        sila_service = SiLAService()

        # Register feature
        server.register_feature(sila_service)
        cloud_server.context = server

        # Assert that the method returns the correct value
        assert cloud_server.context == server
        assert cloud_server.protobuf == server.protobuf
        assert cloud_server.binary_transfer_handler == server.binary_transfer_handler
        assert cloud_server.get_feature(sila_service.fully_qualified_identifier) == sila_service


class TestConfig:
    async def test_defaults(self):
        cloud_server = CloudServer()
        assert cloud_server._config.hostname == "localhost"
        assert cloud_server._config.port == 50_000
        assert cloud_server._config.tls is True
        assert cloud_server._config.root_certificates is None
        assert cloud_server._config.certificate_chain is None
        assert cloud_server._config.private_key is None
        assert cloud_server._config.reconnect_delay == 10000.0
        assert cloud_server._config.options == ChannelOptions()

    async def test_should_warn_on_dict(self):
        # Create server
        reconnect_delay = 1000
        with pytest.warns(
            DeprecationWarning,
            match=(
                "Providing CloudServerConfig as a dictionary is deprecated and will be removed in a future release. "
                "Please provide a CloudServerConfig instance instead."
            ),
        ):
            cloud_server = CloudServer({"reconnect_delay": reconnect_delay})

        assert cloud_server._config.reconnect_delay == reconnect_delay


class TestStart:
    async def test_should_create_channel(self):
        # Create server
        stream_stream = unittest.mock.Mock(spec=grpc.StreamStreamMultiCallable, return_value=AsyncIterator([]))
        channel = unittest.mock.Mock(spec=grpc.aio.Channel, stream_stream=lambda *args, **kwargs: stream_stream)
        config = CloudServerConfig(options={"grpc.keepalive_time_ms": 1000})

        cloud_server = CloudServer(config)

        # Start cloud server
        with unittest.mock.patch("sila.server.cloud_server.create_channel", return_value=channel) as create_channel:
            await cloud_server.start()

        # Assert that the method returns the correct value
        create_channel.assert_called_once_with("localhost:50000", **dataclasses.asdict(config))

    async def test_should_open_bidirectional_stream(self):
        # Create server
        test = unittest.mock.Mock(
            return_value=unittest.mock.Mock(spec=grpc.StreamStreamMultiCallable, return_value=AsyncIterator([]))
        )
        channel = unittest.mock.Mock(spec=grpc.aio.Channel, stream_stream=test)
        cloud_server = CloudServer()

        # Start cloud server
        with unittest.mock.patch("sila.server.cloud_server.create_channel", return_value=channel):
            await cloud_server.start()

        # Assert that the method returns the correct value
        test.assert_called_once_with(
            method="/sila2.org.silastandard.CloudClientEndpoint/ConnectSiLAServer",
            request_serializer=unittest.mock.ANY,
            response_deserializer=unittest.mock.ANY,
        )

    async def test_should_receive_request(self):
        # Create server
        message = ClientMessage()
        stream_stream = unittest.mock.Mock(spec=grpc.StreamStreamMultiCallable, return_value=AsyncIterator([message]))
        channel = unittest.mock.Mock(spec=grpc.aio.Channel, stream_stream=lambda *args, **kwargs: stream_stream)
        cloud_server = CloudServer()
        cloud_server.receive = unittest.mock.AsyncMock()

        # Start cloud server
        with unittest.mock.patch("sila.server.cloud_server.create_channel", return_value=channel):
            await cloud_server.start()
            await asyncio.sleep(0)

        # Assert that the method returns the correct value
        cloud_server.receive.assert_awaited_once_with(message)

    async def test_should_receive_multiple_requests(self):
        # Create server
        message_0 = ClientMessage()
        message_1 = ClientMessage()
        message_2 = ClientMessage()
        stream_stream = unittest.mock.Mock(
            spec=grpc.StreamStreamMultiCallable, return_value=AsyncIterator([message_0, message_1, message_2])
        )
        channel = unittest.mock.Mock(spec=grpc.aio.Channel, stream_stream=lambda *args, **kwargs: stream_stream)
        cloud_server = CloudServer()
        cloud_server.receive = unittest.mock.AsyncMock()

        # Start cloud server
        with unittest.mock.patch("sila.server.cloud_server.create_channel", return_value=channel):
            await cloud_server.start()
            await asyncio.sleep(0)

        # Assert that the method returns the correct value
        assert cloud_server.receive.await_args_list == [
            unittest.mock.call(message_0),
            unittest.mock.call(message_1),
            unittest.mock.call(message_2),
        ]

    async def test_should_handle_cancel(self):
        # Create server
        async def stream():
            with pytest.raises(asyncio.CancelledError) as error:
                await asyncio.sleep(1)
                yield ClientMessage()

            raise error.value

        stream_stream = unittest.mock.Mock(spec=grpc.StreamStreamMultiCallable, return_value=stream())
        channel = unittest.mock.Mock(spec=grpc.aio.Channel, stream_stream=lambda *args, **kwargs: stream_stream)
        cloud_server = CloudServer()

        # Start cloud server
        async def start():
            with unittest.mock.patch("sila.server.cloud_server.create_channel", return_value=channel):
                await cloud_server.start()

        task = asyncio.create_task(start())
        await asyncio.sleep(0)
        task.cancel()
        await asyncio.sleep(0)

        # Assert that the method returns the correct value
        task.result()
        await cloud_server.stop()

    async def test_should_fail_on_connection_error(self):
        # Create server
        stream_stream = unittest.mock.Mock(
            spec=grpc.StreamStreamMultiCallable,
            side_effect=[grpc.aio.AioRpcError(grpc.StatusCode.ABORTED, grpc.aio.Metadata(), grpc.aio.Metadata())],
        )
        channel = unittest.mock.Mock(spec=grpc.aio.Channel, stream_stream=lambda *args, **kwargs: stream_stream)
        cloud_server = CloudServer(CloudServerConfig(reconnect_delay=0))
        cloud_server.receive = unittest.mock.AsyncMock()

        # Start cloud server
        with unittest.mock.patch("sila.server.cloud_server.create_channel", return_value=channel):
            await cloud_server.start()

        assert cloud_server._shutdown.is_set()

    async def test_should_retry_on_communication_error(self):
        # Create server
        message = ClientMessage()

        async def stream():
            raise grpc.aio.AioRpcError(grpc.StatusCode.ABORTED, grpc.aio.Metadata(), grpc.aio.Metadata())
            yield ClientMessage()

        stream_stream = unittest.mock.Mock(
            spec=grpc.StreamStreamMultiCallable, side_effect=[stream(), AsyncIterator([message])]
        )
        channel = unittest.mock.Mock(spec=grpc.aio.Channel, stream_stream=lambda *args, **kwargs: stream_stream)
        cloud_server = CloudServer(CloudServerConfig(reconnect_delay=0))
        cloud_server.receive = unittest.mock.AsyncMock()

        # Start cloud server
        with unittest.mock.patch("sila.server.cloud_server.create_channel", return_value=channel):
            await cloud_server.start()
            await asyncio.sleep(0)
            await cloud_server.wait_for_ready()

        # Assert that the method returns the correct value
        assert cloud_server.receive.await_args_list == [unittest.mock.call(message)]


class TestStop:
    async def test_should_close_channel(self):
        # Create server
        cloud_server = CloudServer()
        _channel = cloud_server._channel = unittest.mock.Mock(spec=grpc.aio.Channel)

        # Stop cloud server
        await cloud_server.stop()

        # Assert that the method returns the correct value
        _channel.close.assert_called_once_with(grace=None)

    async def test_should_close_channel_with_grace(self):
        # Create server
        cloud_server = CloudServer()
        _channel = cloud_server._channel = unittest.mock.Mock(spec=grpc.aio.Channel)

        # Stop cloud server
        await cloud_server.stop(grace=1000)

        # Assert that the method returns the correct value
        _channel.close.assert_called_once_with(grace=1000)

    async def test_should_cancel_subscriptions(self):
        # Create server
        async def subscription():
            with pytest.raises(asyncio.CancelledError):
                await asyncio.sleep(1)

        cloud_server = CloudServer()
        cloud_server._channel = unittest.mock.Mock(spec=grpc.aio.Channel)
        task = cloud_server._tasks["subscription"] = asyncio.create_task(subscription(), name="subscription")

        # Stop cloud server
        await cloud_server.stop()
        await asyncio.sleep(0)

        # Assert that the method returns the correct value
        assert task.done()


class TestDeserializeResponse:
    async def test_should_ignore_empty_client_messages(self):
        # Create server
        cloud_server = CloudServer()

        # Deserialize response
        message = cloud_server._deserialize_response(b"")

        # Assert that the method returns the correct value
        assert message == ClientMessage(request_uuid=unittest.mock.ANY)

    async def test_should_ignore_invalid_client_messages(self):
        # Create server
        cloud_server = CloudServer()

        # Deserialize response
        message = cloud_server._deserialize_response(b"invlida")

        # Assert that the method returns the correct value
        assert message == ClientMessage(request_uuid=unittest.mock.ANY)


class TestSerializeRequest:
    async def test_should_ignore_empty_server_messages(self):
        # Create server
        cloud_server = CloudServer()
        message = ServerMessage()

        # Serialize request
        buffer = cloud_server._serialize_request(message)

        # Assert that the method returns the correct value
        assert buffer == b"\x0a\x24" + message.request_uuid.encode()

    async def test_should_ignore_invalid_server_messages(self):
        # Create server
        cloud_server = CloudServer()
        message = ServerMessage()
        message.encode = unittest.mock.Mock(side_effect=EncodeError("encode error"))

        # Serialize request
        buffer = cloud_server._serialize_request(message)

        # Assert that the method returns the correct value
        assert buffer == b""
