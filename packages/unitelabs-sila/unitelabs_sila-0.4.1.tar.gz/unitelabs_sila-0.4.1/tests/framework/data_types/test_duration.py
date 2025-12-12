import re
import unittest.mock

import pytest
import typing_extensions as typing

from sila import datetime
from sila.framework.data_types.duration import Duration

NATIVE_TEST_CASES = [
    pytest.param(Duration(seconds=1), datetime.timedelta(seconds=1), id="1s"),
    pytest.param(Duration(seconds=0, nanos=1000), datetime.timedelta(seconds=0, microseconds=1), id="0s 1μs"),
    pytest.param(Duration(seconds=1, nanos=1000), datetime.timedelta(seconds=1, microseconds=1), id="1s 1μs"),
    pytest.param(Duration(seconds=0, nanos=999999000), datetime.timedelta(seconds=1, microseconds=-1), id="1s -1μs"),
    pytest.param(Duration(seconds=12, nanos=34000), datetime.timedelta(seconds=12, microseconds=34), id="12s 34μs"),
    pytest.param(Duration(seconds=86399999999999, nanos=999999000), datetime.timedelta.max, id="max"),
]
ENCODE_TEST_CASES = [
    pytest.param(Duration(seconds=1), b"\x08\x01", id="1: 1"),
    pytest.param(Duration(seconds=-1), b"\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01", id="1: -1"),
    pytest.param(Duration(seconds=1, nanos=1000), b"\x08\x01\x10\xe8\x07", id="1: 1, 2: 1000"),
    pytest.param(Duration(seconds=0, nanos=1000), b"\x10\xe8\x07", id="2: 1000"),
    pytest.param(
        Duration(seconds=-1, nanos=1000),
        b"\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\xe8\x07",
        id="1: -1, 2: 1000",
    ),
    pytest.param(Duration(seconds=0, nanos=999999000), b"\x10\x98\x8c\xeb\xdc\x03", id="2: 999999000"),
    pytest.param(
        Duration(seconds=-1, nanos=999999000),
        b"\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\x98\x8c\xeb\xdc\x03",
        id="1: -1, 2: 999999000",
    ),
    pytest.param(
        Duration(seconds=-2, nanos=999999000),
        b"\x08\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\x98\x8c\xeb\xdc\x03",
        id="1: -2, 2: 999999000",
    ),
    pytest.param(Duration(seconds=12, nanos=34000), b"\x08\x0c\x10\xd0\x89\x02", id="1: 12, 2: 34000"),
    pytest.param(Duration(seconds=-86399999913600), b"\x08\x80\xa3\xc9\xf5\xb6\xad\xec\xff\xff\x01", id="min"),
    pytest.param(
        Duration(seconds=86399999999999, nanos=999999000),
        b"\x08\xff\xff\xbb\x8a\xc9\xd2\x13\x10\x98\x8c\xeb\xdc\x03",
        id="max",
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(Duration(), b"", id="1: 0"),
    pytest.param(Duration(), b"", id="2: 0"),
    pytest.param(Duration(), b"\x18\x00", id="3: 0"),
    pytest.param(Duration(), b"", id="1: 0, 2: 0"),
    pytest.param(Duration(), b"\x18\x00", id="1: 0, 3: 0"),
    pytest.param(Duration(), b"", id="2: 0, 1: 0"),
    pytest.param(Duration(), b"\x18\x00", id="2: 0, 3: 0"),
    pytest.param(Duration(), b"\x18\x00", id="3: 0, 1: 0"),
    pytest.param(Duration(), b"\x18\x00", id="3: 0, 2: 0"),
    pytest.param(Duration(), b"\x18\x00", id="1: 0, 2: 0, 3: 0"),
    pytest.param(Duration(), b"\x18\x00", id="1: 0, 3: 0, 2: 0"),
    pytest.param(Duration(), b"\x18\x00", id="2: 0, 1: 0, 3: 0"),
    pytest.param(Duration(), b"\x18\x00", id="2: 0, 3: 0, 1: 0"),
    pytest.param(Duration(), b"\x18\x00", id="3: 0, 1: 0, 2: 0"),
    pytest.param(Duration(), b"\x18\x00", id="3: 0, 2: 0, 1: 0"),
    pytest.param(Duration(seconds=12), b"\x08\x0c", id="1: 12"),
    pytest.param(Duration(seconds=12), b"\x08\x0c", id="1: 12, 2: 0"),
    pytest.param(Duration(seconds=12), b"\x08\x0c\x18\x00", id="1: 12, 3: 0"),
    pytest.param(Duration(seconds=12), b"\x08\x0c", id="2: 0, 1: 12"),
    pytest.param(Duration(seconds=12), b"\x18\x00\x08\x0c", id="3: 0, 1: 12"),
    pytest.param(Duration(seconds=12), b"\x08\x0c\x18\x00", id="1: 12, 2: 0, 3: 0"),
    pytest.param(Duration(seconds=12), b"\x08\x0c\x18\x00", id="1: 12, 3: 0, 2: 0"),
    pytest.param(Duration(seconds=12), b"\x08\x0c\x18\x00", id="2: 0, 1: 12, 3: 0"),
    pytest.param(Duration(seconds=12), b"\x18\x00\x08\x0c", id="2: 0, 3: 0, 1: 12"),
    pytest.param(Duration(seconds=12), b"\x18\x00\x08\x0c", id="3: 0, 1: 12, 2: 0"),
    pytest.param(Duration(seconds=12), b"\x18\x00\x08\x0c", id="3: 0, 2: 0, 1: 12"),
    pytest.param(Duration(nanos=34000), b"\x10\xd0\x89\x02", id="2: 34000"),
    pytest.param(Duration(nanos=34000), b"\x10\xd0\x89\x02", id="1: 0, 2: 34000"),
    pytest.param(Duration(nanos=34000), b"\x10\xd0\x89\x02", id="2: 34000, 1: 0"),
    pytest.param(Duration(nanos=34000), b"\x10\xd0\x89\x02\x18\x00", id="2: 34000, 3: 0"),
    pytest.param(Duration(nanos=34000), b"\x18\x00\x10\xd0\x89\x02", id="3: 0, 2: 34000"),
    pytest.param(Duration(nanos=34000), b"\x10\xd0\x89\x02\x18\x00", id="1: 0, 2: 34000, 3: 0"),
    pytest.param(Duration(nanos=34000), b"\x18\x00\x10\xd0\x89\x02", id="1: 0, 3: 0, 2: 34000"),
    pytest.param(Duration(nanos=34000), b"\x10\xd0\x89\x02\x18\x00", id="2: 34000, 1: 0, 3: 0"),
    pytest.param(Duration(nanos=34000), b"\x10\xd0\x89\x02\x18\x00", id="2: 34000, 3: 0, 1: 0"),
    pytest.param(Duration(nanos=34000), b"\x18\x00\x10\xd0\x89\x02", id="3: 0, 1: 0, 2: 34000"),
    pytest.param(Duration(nanos=34000), b"\x18\x00\x10\xd0\x89\x02", id="3: 0, 2: 34000, 1: 0"),
    pytest.param(Duration(seconds=12, nanos=34000), b"\x08\x0c\x10\xd0\x89\x02", id="1: 12, 2: 34000"),
    pytest.param(Duration(seconds=12, nanos=34000), b"\x10\xd0\x89\x02\x08\x0c", id="2: 34000, 1: 12"),
    pytest.param(Duration(seconds=12, nanos=34000), b"\x08\x0c\x10\xd0\x89\x02\x18\x00", id="1: 12, 2: 34000, 3: 0"),
    pytest.param(Duration(seconds=12, nanos=34000), b"\x08\x0c\x18\x00\x10\xd0\x89\x02", id="1: 12, 3: 0, 2: 34000"),
    pytest.param(Duration(seconds=12, nanos=34000), b"\x10\xd0\x89\x02\x08\x0c\x18\x00", id="2: 34000, 1: 12, 3: 0"),
    pytest.param(Duration(seconds=12, nanos=34000), b"\x10\xd0\x89\x02\x18\x00\x08\x0c", id="2: 34000, 3: 0, 1: 12"),
    pytest.param(Duration(seconds=12, nanos=34000), b"\x18\x00\x08\x0c\x10\xd0\x89\x02", id="3: 0, 1: 12, 2: 34000"),
    pytest.param(Duration(seconds=12, nanos=34000), b"\x18\x00\x10\xd0\x89\x02\x08\x0c", id="3: 0, 2: 34000, 1: 12"),
]


class TestTotalSeconds:
    @pytest.mark.parametrize(
        ("duration", "total_seconds"),
        [
            pytest.param(Duration(), 0, id="0"),
            pytest.param(Duration(seconds=12, nanos=34000), 12.000034, id="12.000034"),
            pytest.param(Duration(seconds=1, nanos=999999999), 1.999999999, id="1.999999999"),
            pytest.param(Duration(seconds=-1, nanos=-999999999), -1.999999999, id="-1.999999999"),
        ],
    )
    async def test_should_return_total_seconds(self, duration: Duration, total_seconds: float):
        # Assert that the method returns the correct value
        assert duration.total_seconds == total_seconds

    @pytest.mark.parametrize(
        ("duration", "total_seconds"),
        [
            pytest.param(Duration(), 0, id="0"),
            pytest.param(Duration(seconds=12, nanos=34000), 12.000034, id="12.000034"),
            pytest.param(Duration(seconds=2), 1.9999999999, id="1.9999999999"),
            pytest.param(Duration(seconds=-2), -1.9999999999, id="-1.9999999999"),
        ],
    )
    async def test_should_create_duration_from_total_seconds(self, duration: Duration, total_seconds: float):
        # Assert that the method returns the correct value
        assert Duration.from_total_seconds(total_seconds) == duration


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Duration.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Duration()

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: Duration, native: datetime.timedelta):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Duration.from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_accept_seconds(self):
        # Create data type
        context = unittest.mock.Mock()
        assert await Duration.from_native(context, seconds=12) == Duration(seconds=12)

    async def test_should_raise_on_invalid_seconds_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected seconds of type 'int', received 'str'.")):
            await Duration.from_native(context, seconds=typing.cast(int, ""))

    async def test_should_raise_on_invalid_seconds_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Seconds must be a positive number, received '-1'.")):
            await Duration.from_native(context, seconds=-1)

    async def test_should_accept_nanos(self):
        # Create data type
        context = unittest.mock.Mock()
        assert await Duration.from_native(context, nanos=34) == Duration(nanos=34)

    async def test_should_raise_on_invalid_nanos_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected nanos of type 'int', received 'str'.")):
            await Duration.from_native(context, nanos=typing.cast(int, ""))

    async def test_should_raise_on_invalid_nanos_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Nanos must be between 0 and 1e+9, received '-1'.")):
            await Duration.from_native(context, nanos=-1)


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Duration, native: datetime.timedelta):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_seconds_type(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected seconds of type 'int', received 'str'.")):
            await Duration(seconds=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_seconds_value(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Seconds must be a positive number, received '-1'.")):
            await Duration(seconds=-1).to_native(context)

    async def test_should_raise_on_invalid_nanos_type(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected nanos of type 'int', received 'str'.")):
            await Duration(nanos=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_nanos_value(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Nanos must be between 0 and 1e+9, received '-1'.")):
            await Duration(nanos=-1).to_native(context)


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode data type
        message = Duration.decode(b"")

        # Assert that the method returns the correct value
        assert message == Duration()

    @pytest.mark.parametrize(("data_type", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Duration, buffer: bytes):
        # Decode data type
        message = Duration.decode(buffer)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = Duration.decode(b"\x08\x01\x08\x00")

        # Assert that the method returns the correct value
        assert message == Duration(seconds=0)

    async def test_should_decode_limited_buffer(self):
        # Decode data type
        message = Duration.decode(
            b"\x08\x01\x08\x00",
            len(b"\x08\x01"),
        )

        # Assert that the method returns the correct value
        assert message == Duration(seconds=1)


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Duration().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Duration, buffer: bytes):
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
        data_type = Duration()
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestEquality:
    @pytest.mark.parametrize(("seconds", "nanos"), [(0, 0), (-12, 34), (12, 34)])
    def test_should_compare_equality(self, seconds: int, nanos: int):
        assert Duration(seconds=seconds, nanos=nanos) == Duration(seconds=seconds, nanos=nanos)

    def test_should_compare_inequality(self):
        assert Duration(seconds=0, nanos=0) != object()


class TestOrder:
    @pytest.mark.parametrize(
        ("data_type_0", "data_type_1", "lt", "le", "gt", "ge"),
        [
            (Duration(seconds=0, nanos=0), Duration(seconds=0, nanos=0), False, True, False, True),
            (
                Duration(seconds=-12, nanos=34),
                Duration(seconds=0, nanos=0),
                True,
                True,
                False,
                False,
            ),
            (
                Duration(seconds=12, nanos=34),
                Duration(seconds=0, nanos=0),
                False,
                False,
                True,
                True,
            ),
        ],
    )
    def test_should_compare_order_to_date(
        self, data_type_0: Duration, data_type_1: Duration, lt: bool, le: bool, gt: bool, ge: bool
    ):
        assert (data_type_0 < data_type_1) is lt
        assert (data_type_0 <= data_type_1) is le
        assert (data_type_0 > data_type_1) is gt
        assert (data_type_0 >= data_type_1) is ge

    def test_should_ignore_comparison_to_object(self):
        with pytest.raises(TypeError):
            assert Duration(seconds=0, nanos=0) < object()

        with pytest.raises(TypeError):
            assert Duration(seconds=0, nanos=0) <= object()

        with pytest.raises(TypeError):
            assert Duration(seconds=0, nanos=0) > object()

        with pytest.raises(TypeError):
            assert Duration(seconds=0, nanos=0) >= object()


class TestHash:
    def test_should_hash_constrained(self):
        # Create data type
        data_type_0 = Duration(seconds=12, nanos=34)
        data_type_1 = Duration(seconds=12, nanos=34)

        # Hash data type
        assert hash(data_type_0) == hash(data_type_1)
