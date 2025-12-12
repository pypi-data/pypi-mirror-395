import math
import re
import sys
import textwrap
import unittest.mock

import pytest
import typing_extensions as typing

from sila.framework.data_types.real import Real
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer

NATIVE_TEST_CASES = [
    pytest.param(Real(value=0.1), 0.1, id="0.1"),
    pytest.param(Real(value=-0.1), -0.1, id="-0.1"),
    pytest.param(Real(value=3.141592653589793), math.pi, id="pi"),
    pytest.param(Real(value=2.2250738585072014e-308), sys.float_info.min, id="min"),
    pytest.param(Real(value=1.7976931348623157e308), sys.float_info.max, id="max"),
]
ENCODE_TEST_CASES = [
    pytest.param(Real(value=0.1), b"\x09\x9a\x99\x99\x99\x99\x99\xb9\x3f", id="1: 0.1"),
    pytest.param(Real(value=-0.1), b"\x09\x9a\x99\x99\x99\x99\x99\xb9\xbf", id="1: -0.1"),
    pytest.param(Real(value=math.pi), b"\x09\x18\x2d\x44\x54\xfb\x21\x09\x40", id="1: 3.141592653589793"),
    pytest.param(Real(value=sys.float_info.min), b"\x09\x00\x00\x00\x00\x00\x00\x10\x00", id="min"),
    pytest.param(Real(value=sys.float_info.max), b"\x09\xff\xff\xff\xff\xff\xff\xef\x7f", id="max"),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(Real(), b"\t\x00\x00\x00\x00\x00\x00\x00\x00", id="1: 0"),
    pytest.param(Real(), b"\x10\x00", id="2: 0"),
    pytest.param(Real(), b"\t\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00", id="1: 0, 2: 0"),
    pytest.param(Real(), b"\x10\x00\t\x00\x00\x00\x00\x00\x00\x00\x00", id="2: 0, 1: 0"),
    pytest.param(Real(value=math.pi), b"\t\x18-DT\xfb!\t@", id="1: 3.141592653589793"),
    pytest.param(Real(value=math.pi), b"\t\x18-DT\xfb!\t@\x10\x00", id="1: 3.141592653589793, 2: 0"),
    pytest.param(Real(value=math.pi), b"\x10\x00\t\x18-DT\xfb!\t@", id="2: 0, 1: 3.141592653589793"),
]


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Real.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Real()

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: Real, native: float):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Real.from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected value of type 'float', received 'str'.")):
            await Real.from_native(context, typing.cast(float, ""))


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Real, native: float):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_type(self):
        # Create data type
        context = unittest.mock.Mock()

        # Convert data type
        with pytest.raises(TypeError, match=re.escape("Expected value of type 'float', received 'str'.")):
            await Real(typing.cast(float, "")).to_native(context)


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode data type
        message = Real.decode(b"")

        # Assert that the method returns the correct value
        assert message == Real()

    @pytest.mark.parametrize(("data_type", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Real, buffer: bytes):
        # Decode data type
        message = Real.decode(buffer)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = Real.decode(b"\x09\x00\x00\x00\x00\x00\x00\xf0\x3f\x09\x00\x00\x00\x00\x00\x00\x00\x00")

        # Assert that the method returns the correct value
        assert message == Real(value=0)

    async def test_should_decode_limited_buffer(self):
        # Decode data type
        message = Real.decode(b"\x09\x00\x00\x00\x00\x00\x00\xf0\x3f\x09\x00\x00\x00\x00\x00\x00\x00\x00", 9)

        # Assert that the method returns the correct value
        assert message == Real(value=1)


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Real().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Real, buffer: bytes):
        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x00", id="default"),
            pytest.param(2, b"\x12\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode data type
        data_type = Real()
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Serialize
        xml = Serializer.serialize(Real.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<DataType><Basic>Real</Basic></DataType>"

    async def test_should_deserialize_multiline_xml(self):
        # Serialize
        xml = Serializer.serialize(Real.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Basic>Real</Basic>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Basic>Real</Basic>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, Real.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Real

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Basic>
            Real
        </Basic>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Real.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Real

    async def test_should_raise_on_unknown_basic_type(self):
        # Create xml
        xml = "<Basic>Complex</Basic>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, Real.deserialize)


class TestStringify:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Real(), "0", id="0"),
            pytest.param(Real(value=math.pi), "3.141592653589793", id="pi"),
            pytest.param(Real(value=sys.float_info.min), "2.2250738585072014e-308", id="min"),
            pytest.param(Real(value=sys.float_info.max), "1.7976931348623157e+308", id="max"),
        ],
    )
    def test_should_return_string(self, data_type: Real, value: str):
        # Convert data type
        assert f"{data_type}" == value


class TestEquality:
    @pytest.mark.parametrize(
        ("value"),
        [
            pytest.param(0, id="0"),
            pytest.param(math.pi, id="pi"),
            pytest.param(sys.float_info.min, id="min"),
            pytest.param(sys.float_info.max, id="max"),
        ],
    )
    def test_should_compare_equality(self, value: float):
        assert Real(value) == Real(value)

    def test_should_compare_inequality(self):
        assert Real(value=3.3) != object()


class TestOrder:
    @pytest.mark.parametrize(
        ("data_type_0", "data_type_1", "lt", "le", "gt", "ge"),
        [
            pytest.param(Real(3.3), Real(3.3), False, True, False, True, id="3.3|3.3"),
            pytest.param(Real(3.3), Real(3.4), True, True, False, False, id="3.3|3.4"),
            pytest.param(Real(3.4), Real(3.3), False, False, True, True, id="3.4|3.3"),
        ],
    )
    def test_should_order_reals(self, data_type_0: Real, data_type_1: Real, lt: bool, le: bool, gt: bool, ge: bool):
        assert (data_type_0 < data_type_1) is lt
        assert (data_type_0 <= data_type_1) is le
        assert (data_type_0 > data_type_1) is gt
        assert (data_type_0 >= data_type_1) is ge

    def test_should_ignore_comparison_to_object(self):
        with pytest.raises(TypeError):
            assert (Real(3.3) < object()) is False

        with pytest.raises(TypeError):
            assert (Real(3.3) <= object()) is False

        with pytest.raises(TypeError):
            assert (Real(3.3) > object()) is False

        with pytest.raises(TypeError):
            assert (Real(3.3) >= object()) is False


class TestHash:
    def test_should_hash_constrained(self):
        # Create data type
        data_type_0 = Real(value=3.141592653589793)
        data_type_1 = Real(value=3.141592653589793)

        # Hash data type
        assert hash(data_type_0) == hash(data_type_1)
