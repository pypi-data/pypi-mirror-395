import re
import unittest.mock

import grpc
import pytest

from sila.framework.data_types.element import Element
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.string import String
from sila.framework.data_types.structure import Structure
from sila.framework.protobuf.conversion_error import ConversionError
from sila.framework.protobuf.decode_error import DecodeError
from sila.framework.protobuf.protobuf import Protobuf


class TestRegisterMessage:
    def test_should_accept_elements(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)

        # Register message
        data_type = {"key": Element(identifier="Key", display_name="Key", data_type=String)}
        message = protobuf.register_message(name="MessageName", message=data_type)

        # Assert that the method returns the correct value
        assert issubclass(message, Structure)
        assert message.__name__ == "MessageName"
        assert message.elements == data_type

    def test_should_accept_structure(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)

        # Register message
        data_type = Structure.create(
            name="MessageName", elements={"key": Element(identifier="Key", display_name="Key", data_type=String)}
        )
        message = protobuf.register_message(message=data_type)

        # Assert that the method returns the correct value
        assert issubclass(message, Structure)
        assert message.__name__ == "MessageName"
        assert message.elements == data_type.elements

    def test_should_accept_description(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)

        # Register message
        package = "sila2.org.silastandard"
        description = "Some details about the protobuf message."
        data_type = {"key": Element(identifier="Key", display_name="Key", data_type=String)}
        message = protobuf.register_message(
            name="MessageName", package=package, message=data_type, description=description
        )

        # Assert that the method returns the correct value
        assert issubclass(message, Structure)
        assert message.__name__ == "MessageName"
        assert message.__doc__ == description
        assert message.elements == data_type

    def test_should_accept_package(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)

        # Register message
        package = "sila2.org.silastandard"
        data_type = {"key": Element(identifier="Key", display_name="Key", data_type=String)}
        message = protobuf.register_message(name="MessageName", message=data_type, package=package)

        # Assert that the method returns the correct value
        assert issubclass(message, Structure)
        assert message.__name__ == "MessageName"
        assert message.elements == data_type


class TestGetMessage:
    def test_should_find_message_by_name(self):
        # Register Message
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)
        registered_message = protobuf.register_message(
            name="MessageName", message={"key": Element(identifier="Key", display_name="Key", data_type=String)}
        )

        # Get message
        message = protobuf.get_message("MessageName")

        # Assert that the method returns the correct value
        assert message == registered_message

    def test_should_find_message_by_path(self):
        # Register Message
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)
        registered_message = protobuf.register_message(
            name="MessageName",
            message={"key": Element(identifier="Key", display_name="Key", data_type=String)},
            package="sila2.org.silastandard",
        )

        # Get message
        message = protobuf.get_message("sila2.org.silastandard.MessageName")

        # Assert that the method returns the correct value
        assert message == registered_message

    def test_should_raise_on_unknown_path(self):
        # Register Message
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)
        protobuf.register_message(
            name="MessageName",
            message={"key": Element(identifier="Key", display_name="Key", data_type=String)},
            package="sila2.org.silastandard",
        )

        # Get message
        with pytest.raises(
            ValueError, match=re.escape("Could not find any message registered under the given path 'Unknown'.")
        ):
            protobuf.get_message("Unknown")


class TestMessages:
    def test_should_return_registered_messages(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)

        # Register protobuf
        message_0 = protobuf.register_message(
            name="Message0", message={"Key0": Element(identifier="Key0", display_name="Key 0", data_type=String)}
        )
        message_1 = protobuf.register_message(
            name="Message1", message={"Key1": Element(identifier="Key1", display_name="Key 1", data_type=String)}
        )
        message_2 = protobuf.register_message(
            name="Message2",
            message={"Key2": Element(identifier="Key2", display_name="Key 2", data_type=String)},
            package="sila2.org.silastandard",
        )

        # Assert that the method returns the correct value
        assert protobuf.messages == {
            "Message0": message_0,
            "Message1": message_1,
            "sila2.org.silastandard.Message2": message_2,
        }


class TestRegisterService:
    def test_should_merge_with_existing_service(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)

        # Register service
        protobuf.register_service(
            name="ServiceName",
            service={
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a),
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b),
            },
            package="sila2.org.silastandard",
        )
        service = protobuf.register_service(
            name="ServiceName",
            service={
                "MethodC": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_c),
            },
            package="sila2.org.silastandard",
        )

        # Assert that the method returns the correct value
        assert service == {
            "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a),
            "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b),
            "MethodC": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_c),
        }

    def test_should_override_existing_service_methods(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)

        # Register service
        protobuf.register_service(
            name="ServiceName",
            service={
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a1),
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b),
            },
            package="sila2.org.silastandard",
        )
        service = protobuf.register_service(
            name="ServiceName",
            service={
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a2),
            },
            package="sila2.org.silastandard",
        )

        # Assert that the method returns the correct value
        assert service == {
            "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a2),
            "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b),
        }

    def test_should_replace_existing_service_when_forced(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)

        # Register service
        protobuf.register_service(
            name="ServiceName",
            service={
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a),
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b),
            },
            package="sila2.org.silastandard",
        )
        service = protobuf.register_service(
            name="ServiceName",
            service={
                "MethodC": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_c),
            },
            package="sila2.org.silastandard",
            force=True,
        )

        # Assert that the method returns the correct value
        assert service == {
            "MethodC": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_c),
        }


class TestServices:
    def test_should_return_registered_services(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)

        # Register services
        protobuf.register_service(
            name="Service1",
            service={
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a),
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b),
            },
        )
        protobuf.register_service(
            name="Service2",
            service={"MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_c)},
            package="sila2.org.silastandard",
        )

        # Assert that the method returns the correct value
        assert protobuf.services == {
            "Service1": {
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a),
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b),
            },
            "sila2.org.silastandard.Service2": {
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_c)
            },
        }


class TestDecode:
    async def test_should_raise_on_unknown_path(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)

        # Decode message
        with pytest.raises(
            ValueError, match=re.escape("Could not find any message registered under the given path 'Unknown'.")
        ):
            await protobuf.decode("Unknown", b"")

    async def test_should_raise_on_malformed_buffer(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)
        protobuf.register_message(
            name="MessageName",
            message={"key": Element(identifier="Key", display_name="Key", data_type=String)},
            package="sila2.org.silastandard",
        )

        # Decode message
        with pytest.raises(DecodeError, match=re.escape("Expected wire type 'LEN', received 'VARINT'.")):
            await protobuf.decode("sila2.org.silastandard.MessageName", b"\x0a\x02\x08\x2a")

    async def test_should_raise_on_invalid_value(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)
        protobuf.register_message(
            name="MessageName",
            message={"key": Element(identifier="Key", display_name="Key", data_type=String)},
            package="sila2.org.silastandard",
        )

        # Decode message
        with pytest.raises(ConversionError, match=re.escape("Missing field 'Key' in message 'MessageName'.")):
            await protobuf.decode("sila2.org.silastandard.MessageName", b"")

    async def test_should_return_decoded_value(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)
        protobuf.register_message(
            name="MessageName",
            message={"key": Element(identifier="Key", display_name="Key", data_type=String)},
            package="sila2.org.silastandard",
        )

        # Decode message
        message = await protobuf.decode("sila2.org.silastandard.MessageName", b"\x0a\x0f\x0a\x0dHello, World!")

        assert message == {"key": "Hello, World!"}


class TestEncode:
    async def test_should_raise_on_unknown_path(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)

        # Decode message
        with pytest.raises(
            ValueError, match=re.escape("Could not find any message registered under the given path 'Unknown'.")
        ):
            await protobuf.encode("Unknown", {})

    async def test_should_raise_on_invalid_value(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)
        protobuf.register_message(
            name="MessageName",
            message={"key": Element(identifier="Key", display_name="Key", data_type=Integer)},
            package="sila2.org.silastandard",
        )

        # Decode message
        with pytest.raises(ConversionError, match=re.escape("Missing field 'Key' in message 'MessageName'.")):
            await protobuf.encode("sila2.org.silastandard.MessageName", {})

    async def test_should_return_encoded_value(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf = Protobuf(context)
        protobuf.register_message(
            name="MessageName",
            message={"key": Element(identifier="Key", display_name="Key", data_type=String)},
            package="sila2.org.silastandard",
        )

        # Decode message
        message = await protobuf.encode("sila2.org.silastandard.MessageName", {"key": "Hello, World!"})

        assert message == b"\x0a\x0f\x0a\x0dHello, World!"


class TestMerge:
    def test_should_merge_registered_messages(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf_0 = Protobuf(context)
        message_0 = protobuf_0.register_message(
            name="Message0", message={"Key0": Element(identifier="Key0", display_name="Key 0", data_type=String)}
        )
        message_1 = protobuf_0.register_message(
            name="Message1",
            message={"Key1": Element(identifier="Key1", display_name="Key 1", data_type=String)},
            package="sila2.org.silastandard",
        )

        protobuf_1 = Protobuf(context)
        message_a = protobuf_1.register_message(
            name="MessageA", message={"KeyA": Element(identifier="KeyA", display_name="Key A", data_type=String)}
        )
        message_b = protobuf_1.register_message(
            name="MessageB",
            message={"KeyB": Element(identifier="KeyB", display_name="Key B", data_type=String)},
            package="sila2.org.silastandard",
        )

        # Merge
        protobuf_0.merge(protobuf_1)

        # Assert that the method returns the correct value
        assert protobuf_0.messages == {
            "Message0": message_0,
            "sila2.org.silastandard.Message1": message_1,
            "MessageA": message_a,
            "sila2.org.silastandard.MessageB": message_b,
        }

    def test_should_override_existing_messages(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf_0 = Protobuf(context)
        protobuf_0.register_message(
            name="Message0", message={"Key0": Element(identifier="Key0", display_name="Key 0", data_type=String)}
        )
        message_1 = protobuf_0.register_message(
            name="Message1",
            message={"Key1": Element(identifier="Key1", display_name="Key 1", data_type=String)},
            package="sila2.org.silastandard",
        )

        protobuf_1 = Protobuf(context)
        message_a = protobuf_1.register_message(
            name="Message0", message={"KeyA": Element(identifier="KeyA", display_name="Key A", data_type=String)}
        )
        message_b = protobuf_1.register_message(
            name="MessageB",
            message={"KeyB": Element(identifier="KeyB", display_name="Key B", data_type=String)},
            package="sila2.org.silastandard",
        )

        # Merge
        protobuf_0.merge(protobuf_1)

        # Assert that the method returns the correct value
        assert protobuf_0.messages == {
            "Message0": message_a,
            "sila2.org.silastandard.Message1": message_1,
            "sila2.org.silastandard.MessageB": message_b,
        }

    def test_should_merge_registered_services(self):
        # Create protobuf
        context = unittest.mock.Mock()
        protobuf_0 = Protobuf(context)
        protobuf_0.register_service(
            name="Service1",
            service={
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a),
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b),
            },
        )
        protobuf_0.register_service(
            name="Service2",
            service={"MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_c)},
            package="sila2.org.silastandard",
        )

        protobuf_1 = Protobuf(context)
        protobuf_1.register_service(
            name="ServiceA",
            service={
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_d),
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_e),
            },
        )
        protobuf_1.register_service(
            name="ServiceB",
            service={"MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_f)},
            package="sila2.org.silastandard",
        )

        # Merge
        protobuf_0.merge(protobuf_1)

        # Assert that the method returns the correct value
        assert protobuf_0.services == {
            "Service1": {
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a),
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b),
            },
            "sila2.org.silastandard.Service2": {
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_c)
            },
            "ServiceA": {
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_d),
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_e),
            },
            "sila2.org.silastandard.ServiceB": {
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_f)
            },
        }

    def test_should_merge_with_existing_services(self):
        # Create protobuf
        context = unittest.mock.Mock()

        protobuf_0 = Protobuf(context)
        protobuf_0.register_service(
            name="Service1",
            service={
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a),
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b1),
            },
        )

        protobuf_1 = Protobuf(context)
        protobuf_1.register_service(
            name="Service1",
            service={
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b2),
                "MethodC": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_c),
            },
        )

        # Merge
        protobuf_0.merge(protobuf_1)

        # Assert that the method returns the correct value
        assert protobuf_0.services == {
            "Service1": {
                "MethodA": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_a),
                "MethodB": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_b2),
                "MethodC": grpc.unary_unary_rpc_method_handler(unittest.mock.sentinel.method_c),
            },
        }
