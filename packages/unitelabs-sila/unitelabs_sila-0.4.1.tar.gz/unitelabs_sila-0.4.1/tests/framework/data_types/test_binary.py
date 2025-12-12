import re
import textwrap
import unittest.mock

import pytest
import typing_extensions as typing

from sila.framework.binary_transfer.binary_transfer_error import InvalidBinaryTransferUUID
from sila.framework.binary_transfer.binary_transfer_handler import BinaryTransferHandler
from sila.framework.common import Context
from sila.framework.data_types.binary import Binary
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer
from sila.framework.protobuf.decode_error import DecodeError

NATIVE_TEST_CASES = [
    pytest.param(Binary(value=b"Hello, World!"), b"Hello, World!", id="Hello, World!"),
    pytest.param(Binary(value=b" " * 2**21), b" " * 2**21, id="max"),
]
ENCODE_TEST_CASES = [
    pytest.param(Binary(value=b"Hello, World!"), b"\x0a\x0dHello, World!", id="1: {Hello, World!}"),
    pytest.param(
        Binary(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x12\x2400000000-0000-0000-0000-000000000000",
        id='2: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(Binary(value=b" " * 2**21), b"\x0a\x80\x80\x80\x01" + b"\x20" * 2**21, id="max"),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(Binary(), b"\x0a\x00", id='1: {""}'),
    pytest.param(Binary(binary_transfer_uuid=""), b"\x12\x00", id='2: {""}'),
    pytest.param(Binary(binary_transfer_uuid=""), b"\x0a\x00\x12\x00", id='1: {""}, 2: {""}'),
    pytest.param(Binary(), b"\x0a\x00\x18\x00", id='1: {""}, 3: 0'),
    pytest.param(Binary(), b"\x12\x00\x0a\x00", id='2: {""}, 1: {""}'),
    pytest.param(Binary(binary_transfer_uuid=""), b"\x12\x00\x18\x00", id='2: {""}, 3: 0'),
    pytest.param(Binary(), b"\x18\x00\x0a\x00", id='3: 0, 1: {""}'),
    pytest.param(Binary(binary_transfer_uuid=""), b"\x18\x00\x12\x00", id='3: 0, 2: {""}'),
    pytest.param(Binary(binary_transfer_uuid=""), b"\x0a\x00\x12\x00\x18\x00", id='1: {""}, 2: {""}, 3: 0'),
    pytest.param(Binary(binary_transfer_uuid=""), b"\x0a\x00\x18\x00\x12\x00", id='1: {""}, 3: 0, 2: {""}'),
    pytest.param(Binary(), b"\x12\x00\x0a\x00\x18\x00", id='2: {""}, 1: {""}, 3: 0'),
    pytest.param(Binary(), b"\x12\x00\x18\x00\x0a\x00", id='2: {""}, 3: 0, 1: {""}'),
    pytest.param(Binary(binary_transfer_uuid=""), b"\x18\x00\x0a\x00\x12\x00", id='3: 0, 1: {""}, 2: {""}'),
    pytest.param(Binary(), b"\x18\x00\x12\x00\x0a\x00", id='3: 0, 2: {""}, 1: {""}'),
    pytest.param(Binary(value=b"Hello, World!"), b"\x0a\rHello, World!", id='1: {"Hello, World!"}'),
    pytest.param(Binary(binary_transfer_uuid=""), b"\x0a\rHello, World!\x12\x00", id='1: {"Hello, World!"}, 2: {""}'),
    pytest.param(Binary(value=b"Hello, World!"), b"\x0a\rHello, World!\x18\x00", id='1: {"Hello, World!"}, 3: 0'),
    pytest.param(Binary(value=b"Hello, World!"), b"\x12\x00\x0a\rHello, World!", id='2: {""}, 1: {"Hello, World!"}'),
    pytest.param(Binary(value=b"Hello, World!"), b"\x18\x00\x0a\rHello, World!", id='3: 0, 1: {"Hello, World!"}'),
    pytest.param(
        Binary(binary_transfer_uuid=""),
        b"\x0a\rHello, World!\x12\x00\x18\x00",
        id='1: {"Hello, World!"}, 2: {""}, 3: 0',
    ),
    pytest.param(
        Binary(binary_transfer_uuid=""),
        b"\x0a\rHello, World!\x18\x00\x12\x00",
        id='1: {"Hello, World!"}, 3: 0, 2: {""}',
    ),
    pytest.param(
        Binary(value=b"Hello, World!"), b"\x12\x00\x0a\rHello, World!\x18\x00", id='2: {""}, 1: {"Hello, World!"}, 3: 0'
    ),
    pytest.param(
        Binary(value=b"Hello, World!"), b"\x12\x00\x18\x00\x0a\rHello, World!", id='2: {""}, 3: 0, 1: {"Hello, World!"}'
    ),
    pytest.param(
        Binary(binary_transfer_uuid=""),
        b"\x18\x00\x0a\rHello, World!\x12\x00",
        id='3: 0, 1: {"Hello, World!"}, 2: {""}',
    ),
    pytest.param(
        Binary(value=b"Hello, World!"), b"\x18\x00\x12\x00\x0a\rHello, World!", id='3: 0, 2: {""}, 1: {"Hello, World!"}'
    ),
    pytest.param(
        Binary(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\x00\x12$00000000-0000-0000-0000-000000000000",
        id='1: {""}, 2: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(
        Binary(),
        b"\x12$00000000-0000-0000-0000-000000000000\x0a\x00",
        id='2: {"00000000-0000-0000-0000-000000000000"}, 1: {""}',
    ),
    pytest.param(
        Binary(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x12$00000000-0000-0000-0000-000000000000\x18\x00",
        id='2: {"00000000-0000-0000-0000-000000000000"}, 3: 0',
    ),
    pytest.param(
        Binary(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x18\x00\x12$00000000-0000-0000-0000-000000000000",
        id='3: 0, 2: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(
        Binary(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\x00\x12$00000000-0000-0000-0000-000000000000\x18\x00",
        id='1: {""}, 2: {"00000000-0000-0000-0000-000000000000"}, 3: 0',
    ),
    pytest.param(
        Binary(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\x00\x18\x00\x12$00000000-0000-0000-0000-000000000000",
        id='1: {""}, 3: 0, 2: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(
        Binary(),
        b"\x12$00000000-0000-0000-0000-000000000000\x0a\x00\x18\x00",
        id='2: {"00000000-0000-0000-0000-000000000000"}, 1: {""}, 3: 0',
    ),
    pytest.param(
        Binary(),
        b"\x12$00000000-0000-0000-0000-000000000000\x18\x00\x0a\x00",
        id='2: {"00000000-0000-0000-0000-000000000000"}, 3: 0, 1: {""}',
    ),
    pytest.param(
        Binary(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x18\x00\x0a\x00\x12$00000000-0000-0000-0000-000000000000",
        id='3: 0, 1: {""}, 2: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(
        Binary(),
        b"\x18\x00\x12$00000000-0000-0000-0000-000000000000\x0a\x00",
        id='3: 0, 2: {"00000000-0000-0000-0000-000000000000"}, 1: {""}',
    ),
    pytest.param(
        Binary(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\rHello, World!\x12$00000000-0000-0000-0000-000000000000",
        id='1: {"Hello, World!"}, 2: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(
        Binary(value=b"Hello, World!"),
        b"\x12$00000000-0000-0000-0000-000000000000\x0a\rHello, World!",
        id='2: {"00000000-0000-0000-0000-000000000000"}, 1: {"Hello, World!"}',
    ),
    pytest.param(
        Binary(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\rHello, World!\x12$00000000-0000-0000-0000-000000000000\x18\x00",
        id='1: {"Hello, World!"}, 2: {"00000000-0000-0000-0000-000000000000"}, 3: 0',
    ),
    pytest.param(
        Binary(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x0a\rHello, World!\x18\x00\x12$00000000-0000-0000-0000-000000000000",
        id='1: {"Hello, World!"}, 3: 0, 2: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(
        Binary(value=b"Hello, World!"),
        b"\x12$00000000-0000-0000-0000-000000000000\x0a\rHello, World!\x18\x00",
        id='2: {"00000000-0000-0000-0000-000000000000"}, 1: {"Hello, World!"}, 3: 0',
    ),
    pytest.param(
        Binary(value=b"Hello, World!"),
        b"\x12$00000000-0000-0000-0000-000000000000\x18\x00\x0a\rHello, World!",
        id='2: {"00000000-0000-0000-0000-000000000000"}, 3: 0, 1: {"Hello, World!"}',
    ),
    pytest.param(
        Binary(binary_transfer_uuid="00000000-0000-0000-0000-000000000000"),
        b"\x18\x00\x0a\rHello, World!\x12$00000000-0000-0000-0000-000000000000",
        id='3: 0, 1: {"Hello, World!"}, 2: {"00000000-0000-0000-0000-000000000000"}',
    ),
    pytest.param(
        Binary(value=b"Hello, World!"),
        b"\x18\x00\x12$00000000-0000-0000-0000-000000000000\x0a\rHello, World!",
        id='3: 0, 2: {"00000000-0000-0000-0000-000000000000"}, 1: {"Hello, World!"}',
    ),
]


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Binary.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Binary()

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: Binary, native: bytes):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Binary.from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_accept_large_value(self):
        native = b" " * (2**21 + 1)
        binary_transfer_uuid = "00000000-0000-0000-0000-000000000000"

        # Create context
        set_binary = unittest.mock.AsyncMock(return_value=binary_transfer_uuid)
        context = unittest.mock.Mock(
            spec=Context, binary_transfer_handler=unittest.mock.Mock(spec=BinaryTransferHandler, set_binary=set_binary)
        )

        # Initialize from native
        data_type = await Binary.from_native(context, native)

        # Assert that the method returns the correct value
        set_binary.assert_awaited_once_with(native, None)
        assert data_type == Binary(binary_transfer_uuid=binary_transfer_uuid)

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()

        # Initialize from native
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'bytes', received 'int'.")):
            await Binary.from_native(context, typing.cast(bytes, 0))

    async def test_should_raise_on_missing_context(self):
        # Create data type
        context = unittest.mock.MagicMock(spec=Context)
        type(context).binary_transfer_handler = unittest.mock.PropertyMock(
            side_effect=RuntimeError("Unable to access 'BinaryTransferHandler' on unbound 'Feature'.")
        )

        # Initialize from native
        native = b" " * (2**21 + 1)
        with pytest.raises(
            RuntimeError, match=re.escape("Unable to access 'BinaryTransferHandler' on unbound 'Feature'.")
        ):
            await Binary.from_native(context, native)


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Binary, native: bytes):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_convert_large_value(self):
        native = b" " * (2**21 + 1)
        binary_transfer_uuid = "00000000-0000-0000-0000-000000000000"

        # Create context
        get_binary = unittest.mock.AsyncMock(return_value=native)
        context = unittest.mock.Mock(
            spec=Context, binary_transfer_handler=unittest.mock.Mock(spec=BinaryTransferHandler, get_binary=get_binary)
        )
        data_type = Binary(binary_transfer_uuid=binary_transfer_uuid)

        # Convert data type
        result = await data_type.to_native(context)

        # Assert that the method returns the correct value
        get_binary.assert_awaited_once_with(binary_transfer_uuid)
        assert result == native

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()

        # Convert data type
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'bytes', received 'int'.")):
            await Binary(typing.cast(bytes, 0)).to_native(context)

    async def test_should_raise_on_unknown_binary_transfer_uuid(self):
        binary_transfer_uuid = "00000000-0000-0000-0000-000000000000"

        # Create context
        get_binary = unittest.mock.AsyncMock(
            side_effect=InvalidBinaryTransferUUID("Recevied an unknown 'binary_transfer_uuid'.")
        )
        context = unittest.mock.Mock(
            spec=Context, binary_transfer_handler=unittest.mock.Mock(spec=BinaryTransferHandler, get_binary=get_binary)
        )
        data_type = Binary(binary_transfer_uuid=binary_transfer_uuid)

        # Convert data type
        with pytest.raises(InvalidBinaryTransferUUID, match=re.escape("Recevied an unknown 'binary_transfer_uuid'.")):
            await data_type.to_native(context)


class TestDecode:
    async def test_should_raise_on_empty_buffer(self):
        # Decode data type
        with pytest.raises(DecodeError, match=re.escape("Missing field in message 'Binary'.")):
            Binary.decode(b"")

    @pytest.mark.parametrize(("data_type", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Binary, buffer: bytes):
        # Decode data type
        message = Binary.decode(buffer)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Decode data type
        message = Binary.decode(b"\x0a\x05Hello\x0a\x05World")

        # Assert that the method returns the correct value
        assert message == Binary(value=b"World")

    async def test_should_decode_limited_buffer(self):
        # Decode data type
        message = Binary.decode(b"\x0a\x05Hello\x0a\x05World", 7)

        # Assert that the method returns the correct value
        assert message == Binary(value=b"Hello")


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Binary().encode()

        # Assert that the method returns the correct value
        assert message == b"\x0a\x00"

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Binary, buffer: bytes):
        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x02\x0a\x00", id="default"),
            pytest.param(2, b"\x12\x02\x0a\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode data type
        data_type = Binary()
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Serialize
        xml = Serializer.serialize(Binary.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<DataType><Basic>Binary</Basic></DataType>"

    async def test_should_deserialize_multiline_xml(self):
        # Serialize
        xml = Serializer.serialize(Binary.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Basic>Binary</Basic>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Basic>Binary</Basic>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, Binary.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Binary

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Basic>
            Binary
        </Basic>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Binary.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Binary

    async def test_should_raise_on_unknown_basic_type(self):
        # Create xml
        xml = "<Basic>Complex</Basic>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, Binary.deserialize)


class TestStringify:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Binary(), ""),
            (Binary(value=b"Hello, World!"), "SGVsbG8sIFdvcmxkIQ=="),
        ],
    )
    def test_should_return_string(self, data_type: Binary, value: str):
        # Convert data type
        assert f"{data_type}" == value


class TestEquality:
    @pytest.mark.parametrize(
        ("value"),
        [
            pytest.param(b"Hello, World!", id="Hello, World!"),
        ],
    )
    def test_should_compare_equality(self, value: float):
        assert Binary(value) == Binary(value)

    def test_should_compare_inequality(self):
        assert Binary(b"Hello, World!") != object()


class TestHash:
    def test_should_hash_constrained(self):
        # Create data type
        data_type_0 = Binary(value=b"Hello, World!")
        data_type_1 = Binary(value=b"Hello, World!")

        # Hash data type
        assert hash(data_type_0) == hash(data_type_1)
