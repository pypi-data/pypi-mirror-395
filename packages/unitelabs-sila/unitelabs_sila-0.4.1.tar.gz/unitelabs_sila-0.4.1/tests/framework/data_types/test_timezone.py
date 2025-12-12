import re
import unittest.mock

import pytest
import typing_extensions as typing

from sila import datetime
from sila.framework.data_types.timezone import Timezone

NATIVE_TEST_CASES = [
    pytest.param(Timezone(hours=-14), datetime.timezone(datetime.timedelta(hours=-14, minutes=0)), id="-14:00"),
    pytest.param(
        Timezone(hours=-2, minutes=59), datetime.timezone(datetime.timedelta(hours=-1, minutes=-1)), id="-01:01"
    ),
    pytest.param(Timezone(hours=-1), datetime.timezone(datetime.timedelta(hours=-1, minutes=0)), id="-01:00"),
    pytest.param(
        Timezone(hours=-1, minutes=1), datetime.timezone(datetime.timedelta(hours=-1, minutes=1)), id="-00:59"
    ),
    pytest.param(
        Timezone(hours=-1, minutes=59), datetime.timezone(datetime.timedelta(hours=0, minutes=-1)), id="-00:01"
    ),
    pytest.param(Timezone(minutes=1), datetime.timezone(datetime.timedelta(hours=0, minutes=1)), id="+00:01"),
    pytest.param(
        Timezone(hours=0, minutes=59), datetime.timezone(datetime.timedelta(hours=1, minutes=-1)), id="+00:59"
    ),
    pytest.param(Timezone(hours=1, minutes=0), datetime.timezone(datetime.timedelta(hours=1, minutes=0)), id="+01:00"),
    pytest.param(Timezone(hours=1, minutes=1), datetime.timezone(datetime.timedelta(hours=1, minutes=1)), id="+01:01"),
    pytest.param(
        Timezone(hours=14, minutes=0), datetime.timezone(datetime.timedelta(hours=14, minutes=0)), id="+14:00"
    ),
]
ENCODE_TEST_CASES = [
    pytest.param(Timezone(hours=-14), b"\x08\xf2\xff\xff\xff\xff\xff\xff\xff\xff\x01", id="1: -14"),
    pytest.param(
        Timezone(hours=-2, minutes=59), b"\x08\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\x3b", id="1: -2, 2: 59"
    ),
    pytest.param(Timezone(hours=-1), b"\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01", id="1: -1"),
    pytest.param(
        Timezone(hours=-1, minutes=1), b"\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\x01", id="1: -1, 2: 1"
    ),
    pytest.param(
        Timezone(hours=-1, minutes=59), b"\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\x3b", id="1: -1, 2: 59"
    ),
    pytest.param(Timezone(minutes=1), b"\x10\x01", id="2: 1"),
    pytest.param(Timezone(minutes=59), b"\x10\x3b", id="2: 59"),
    pytest.param(Timezone(hours=1), b"\x08\x01", id="1: 1"),
    pytest.param(Timezone(hours=1, minutes=1), b"\x08\x01\x10\x01", id="1: 1, 2: 1"),
    pytest.param(Timezone(hours=14), b"\x08\x0e", id="1: 14"),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(Timezone(), b"\x08\x00", id="1: 0"),
    pytest.param(Timezone(), b"\x10\x00", id="2: 0"),
    pytest.param(Timezone(), b"\x18\x00", id="3: 0"),
    pytest.param(Timezone(), b"\x08\x00\x10\x00", id="1: 0, 2: 0"),
    pytest.param(Timezone(), b"\x18\x00\x18\x00", id="1: 0, 3: 0"),
    pytest.param(Timezone(), b"\x10\x00\x08\x00", id="2: 0, 1: 0"),
    pytest.param(Timezone(), b"\x10\x00\x18\x00", id="2: 0, 3: 0"),
    pytest.param(Timezone(), b"\x18\x00\x08\x00", id="3: 0, 1: 0"),
    pytest.param(Timezone(), b"\x18\x00\x10\x00", id="3: 0, 2: 0"),
    pytest.param(Timezone(), b"\x08\x00\x10\x00\x18\x00", id="1: 0, 2: 0, 3: 0"),
    pytest.param(Timezone(), b"\x08\x00\x18\x00\x10\x00", id="1: 0, 3: 0, 2: 0"),
    pytest.param(Timezone(), b"\x10\x00\x08\x00\x18\x00", id="2: 0, 1: 0, 3: 0"),
    pytest.param(Timezone(), b"\x10\x00\x18\x00\x08\x00", id="2: 0, 3: 0, 1: 0"),
    pytest.param(Timezone(), b"\x18\x00\x08\x00\x10\x00", id="3: 0, 1: 0, 2: 0"),
    pytest.param(Timezone(), b"\x18\x00\x10\x00\x08\x00", id="3: 0, 2: 0, 1: 0"),
    pytest.param(Timezone(hours=12), b"\x08\x0c", id="1: 12"),
    pytest.param(Timezone(hours=12), b"\x08\x0c\x10\x00", id="1: 12, 2: 0"),
    pytest.param(Timezone(hours=12), b"\x08\x0c\x18\x00", id="1: 12, 3: 0"),
    pytest.param(Timezone(hours=12), b"\x10\x00\x08\x0c", id="2: 0, 1: 12"),
    pytest.param(Timezone(hours=12), b"\x18\x00\x08\x0c", id="3: 0, 1: 12"),
    pytest.param(Timezone(hours=12), b"\x08\x0c\x10\x00\x18\x00", id="1: 12, 2: 0, 3: 0"),
    pytest.param(Timezone(hours=12), b"\x08\x0c\x18\x00\x10\x00", id="1: 12, 3: 0, 2: 0"),
    pytest.param(Timezone(hours=12), b"\x10\x00\x08\x0c\x18\x00", id="2: 0, 1: 12, 3: 0"),
    pytest.param(Timezone(hours=12), b"\x10\x00\x18\x00\x08\x0c", id="2: 0, 3: 0, 1: 12"),
    pytest.param(Timezone(hours=12), b"\x18\x00\x08\x0c\x10\x00", id="3: 0, 1: 12, 2: 0"),
    pytest.param(Timezone(hours=12), b"\x18\x00\x10\x00\x08\x0c", id="3: 0, 2: 0, 1: 12"),
    pytest.param(Timezone(minutes=34), b"\x10\x22", id="2: 34"),
    pytest.param(Timezone(minutes=34), b"\x08\x00\x10\x22", id="1: 0, 2: 34"),
    pytest.param(Timezone(minutes=34), b"\x10\x22\x08\x00", id="2: 34, 1: 0"),
    pytest.param(Timezone(minutes=34), b"\x10\x22\x18\x00", id="2: 34, 3: 0"),
    pytest.param(Timezone(minutes=34), b"\x18\x00\x10\x22", id="3: 0, 2: 34"),
    pytest.param(Timezone(minutes=34), b"\x08\x00\x10\x22\x18\x00", id="1: 0, 2: 34, 3: 0"),
    pytest.param(Timezone(minutes=34), b"\x08\x00\x18\x00\x10\x22", id="1: 0, 3: 0, 2: 34"),
    pytest.param(Timezone(minutes=34), b"\x10\x22\x08\x00\x18\x00", id="2: 34, 1: 0, 3: 0"),
    pytest.param(Timezone(minutes=34), b"\x10\x22\x18\x00\x08\x00", id="2: 34, 3: 0, 1: 0"),
    pytest.param(Timezone(minutes=34), b"\x18\x00\x08\x00\x10\x22", id="3: 0, 1: 0, 2: 34"),
    pytest.param(Timezone(minutes=34), b"\x18\x00\x10\x22\x08\x00", id="3: 0, 2: 34, 1: 0"),
    pytest.param(Timezone(hours=12, minutes=34), b"\x08\x0c\x10\x22", id="1: 12, 2: 34"),
    pytest.param(Timezone(hours=12, minutes=34), b"\x10\x22\x08\x0c", id="2: 34, 1: 12"),
    pytest.param(Timezone(hours=12, minutes=34), b"\x08\x0c\x10\x22\x18\x00", id="1: 12, 2: 34, 3: 0"),
    pytest.param(Timezone(hours=12, minutes=34), b"\x08\x0c\x18\x00\x10\x22", id="1: 12, 3: 0, 2: 34"),
    pytest.param(Timezone(hours=12, minutes=34), b"\x10\x22\x08\x0c\x18\x00", id="2: 34, 1: 12, 3: 0"),
    pytest.param(Timezone(hours=12, minutes=34), b"\x10\x22\x18\x00\x08\x0c", id="2: 34, 3: 0, 1: 12"),
    pytest.param(Timezone(hours=12, minutes=34), b"\x18\x00\x08\x0c\x10\x22", id="3: 0, 1: 12, 2: 34"),
    pytest.param(Timezone(hours=12, minutes=34), b"\x18\x00\x10\x22\x08\x0c", id="3: 0, 2: 34, 1: 12"),
]


class TestInitFromIsoformat:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Timezone(), "Z", id="Z"),
            pytest.param(Timezone(), "+00:00", id="+00:00"),
            pytest.param(Timezone(), "-00:00", id="-00:00"),
            pytest.param(Timezone(hours=-6, minutes=30), "-05:30", id="-05:30"),
            pytest.param(Timezone(hours=-6, minutes=30), "-05:30", id="-05:30"),
            pytest.param(Timezone(hours=5, minutes=30), "+05:30", id="+05:30"),
            pytest.param(Timezone(hours=12, minutes=34), "+12:34", id="+12:34"),
            pytest.param(Timezone(hours=12, minutes=34), "+1234", id="+1234"),
            pytest.param(Timezone(hours=12), "+12", id="+12"),
            pytest.param(Timezone(hours=-13, minutes=26), "-12:34", id="-12:34"),
            pytest.param(Timezone(hours=-13, minutes=26), "-1234", id="-1234"),
            pytest.param(Timezone(hours=-12), "-12", id="-12"),
        ],
    )
    def test_should_accept_valid_value(self, data_type: Timezone, value: str):
        # Create from ISO format
        assert Timezone.from_isoformat(value) == data_type

    def test_should_raise_on_invalid_value(self):
        # Create from ISO format
        with pytest.raises(
            ValueError, match=re.escape("Expected ISO 8601 timezone with format '±hh:mm', received 'invalid'.")
        ):
            Timezone.from_isoformat("invalid")


class TestToIsoformat:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Timezone(), "Z", id="Z"),
            pytest.param(Timezone(hours=12, minutes=34), "+12:34", id="+12:34"),
            pytest.param(Timezone(hours=12), "+12:00", id="+12:00"),
            pytest.param(Timezone(hours=-13, minutes=26), "-12:34", id="-12:34"),
            pytest.param(Timezone(hours=-12), "-12:00", id="-12:00"),
        ],
    )
    def test_should_convert_to_isoformat(self, data_type: Timezone, value: str):
        # Convert to ISO format
        assert data_type.to_isoformat() == value


class TestInitFromNative:
    async def test_should_accept_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Timezone.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Timezone()

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: Timezone, native: datetime.timezone):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Timezone.from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_raise_on_invalid_type(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(
            TypeError, match=re.escape("Expected timezone of type 'datetime.timezone', received 'str'.")
        ):
            await Timezone.from_native(context, typing.cast(datetime.timezone, "invalid"))

    async def test_should_raise_on_invalid_value(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Timezone hours must be between -14 and 14, received '-15'.")):
            await Timezone.from_native(context, datetime.timezone(datetime.timedelta(hours=-15)))


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Timezone, native: datetime.timezone):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_hours_type(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected hours of type 'int', received 'str'.")):
            await Timezone(hours=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_hours_value(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Timezone hours must be between -14 and 14, received '-15'.")):
            await Timezone(hours=-15).to_native(context)

    async def test_should_raise_on_invalid_minutes_type(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected minutes of type 'int', received 'str'.")):
            await Timezone(minutes=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_minutes_value(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Timezone minutes must be between 0 and 59, received '60'.")):
            await Timezone(minutes=60).to_native(context)

    async def test_should_raise_on_value_out_of_bounds(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(
            ValueError, match=re.escape("Timezone must be between -14:00 and 14:00, received '+14:01'.")
        ):
            await Timezone(hours=14, minutes=1).to_native(context)


class TestDecode:
    async def test_should_decode_empty_buffer(self):
        # Decode data type
        message = Timezone.decode(b"")

        # Assert that the method returns the correct value
        assert message == Timezone()

    @pytest.mark.parametrize(("data_type", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Timezone, buffer: bytes):
        # Decode data type
        message = Timezone.decode(buffer)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = Timezone.decode(b"\x08\x01\x08\x00")

        # Assert that the method returns the correct value
        assert message == Timezone()

    async def test_should_decode_limited_buffer(self):
        # Decode data type
        message = Timezone.decode(b"\x08\x01\x08\x00", 2)

        # Assert that the method returns the correct value
        assert message == Timezone(hours=1)


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Timezone().encode()

        # Assert that the method returns the correct value
        assert message == b""

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Timezone, buffer: bytes):
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
        data_type = Timezone()
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestStringify:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Timezone(), "Z", id="Z"),
            pytest.param(Timezone(hours=12, minutes=34), "+12:34", id="+12:34"),
            pytest.param(Timezone(hours=12), "+12:00", id="+12:00"),
            pytest.param(Timezone(hours=-13, minutes=26), "-12:34", id="-12:34"),
            pytest.param(Timezone(hours=-12), "-12:00", id="-12:00"),
        ],
    )
    def test_should_return_string(self, data_type: Timezone, value: str):
        # Convert data type
        assert f"{data_type}" == value


class TestEquality:
    @pytest.mark.parametrize(("hours", "minutes"), [(0, 0), (-13, 26), (12, 34)])
    def test_should_compare_equality(self, hours: int, minutes: int):
        assert Timezone(hours=hours, minutes=minutes) == Timezone(hours=hours, minutes=minutes)

    def test_should_compare_inequality(self):
        assert Timezone() != object()


class TestOrder:
    @pytest.mark.parametrize(
        ("data_type_0", "data_type_1", "lt", "le", "gt", "ge"),
        [
            pytest.param(Timezone(), Timezone(), False, True, False, True, id="equal"),
            pytest.param(
                Timezone(hours=-13, minutes=26),
                Timezone(),
                True,
                True,
                False,
                False,
                id="smaller",
            ),
            pytest.param(
                Timezone(hours=12, minutes=34),
                Timezone(),
                False,
                False,
                True,
                True,
                id="greater",
            ),
        ],
    )
    def test_should_order_timezone(
        self, data_type_0: Timezone, data_type_1: Timezone, lt: bool, le: bool, gt: bool, ge: bool
    ):
        assert (data_type_0 < data_type_1) is lt
        assert (data_type_0 <= data_type_1) is le
        assert (data_type_0 > data_type_1) is gt
        assert (data_type_0 >= data_type_1) is ge

    def test_should_ignore_comparison_to_object(self):
        with pytest.raises(TypeError):
            assert (Timezone() < object()) is False

        with pytest.raises(TypeError):
            assert (Timezone() <= object()) is False

        with pytest.raises(TypeError):
            assert (Timezone() > object()) is False

        with pytest.raises(TypeError):
            assert (Timezone() >= object()) is False
