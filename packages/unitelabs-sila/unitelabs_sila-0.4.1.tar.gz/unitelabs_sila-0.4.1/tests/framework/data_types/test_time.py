import re
import textwrap
import unittest.mock

import pytest
import typing_extensions as typing

from sila import datetime
from sila.framework.data_types.time import Time
from sila.framework.data_types.timezone import Timezone
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer
from sila.framework.protobuf.decode_error import DecodeError

NATIVE_TEST_CASES = [
    pytest.param(
        Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=12, minutes=34)),
        datetime.time(
            hour=12,
            minute=34,
            second=56,
            microsecond=789000,
            tzinfo=datetime.timezone(datetime.timedelta(hours=12, minutes=34)),
        ),
        id="12:34:56.789+12:34",
    ),
]
ENCODE_TEST_CASES = [
    pytest.param(
        Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=12, minutes=34)),
        b"\x08\x38\x10\x22\x18\x0c\x22\x04\x08\x0c\x10\x22\x28\x95\x06",
        id="1: 56, 2: 34, 3: 12, 4: { 1: 12, 2: 34 }, 5: 789",
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(Time(), b"\x22\x00\x30\x00", id="4: {}, 6: 0"),
    pytest.param(
        Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=12, minutes=34)),
        b"\x18\x0c\x10\x22\x08\x38\x28\x95\x06\x22\x04\x08\x0c\x10\x22\x30\x00",
        id="3: 12, 2: 34, 1: 56, 5: 789, 4: { 1: 12, 2: 34 }, 6: 0",
    ),
    pytest.param(
        Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=12, minutes=34)),
        b"\x30\x00\x18\x0c\x10\x22\x08\x38\x28\x95\x06\x22\x04\x08\x0c\x10\x22",
        id="6: 0, 3: 12, 2: 34, 1: 56, 5: 789, 4: { 1: 12, 2: 34 }",
    ),
]


class TestTimestamp:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Time(), 0, id="00:00:00.000"),
            pytest.param(Time(timezone=Timezone(hours=14)), -50_400, id="00:00:00.000+14:00"),
            pytest.param(Time(timezone=Timezone(hours=-14)), 50_400, id="00:00:00.000-14:00"),
            pytest.param(
                Time(hour=23, minute=59, second=59, millisecond=999),
                86_399.999,
                id="23:59:59.999",
            ),
            pytest.param(
                Time(hour=23, minute=59, second=59, millisecond=999, timezone=Timezone(hours=-14)),
                136_799.999,
                id="23:59:59.999-14:00",
            ),
            pytest.param(
                Time(hour=23, minute=59, second=59, millisecond=999, timezone=Timezone(hours=14)),
                35_999.999,
                id="23:59:59.999+14:00",
            ),
        ],
    )
    def test_should_convert_to_timestamp(self, data_type: Time, value: int):
        # Convert data type
        assert data_type.timestamp == value


class TestInitFromIsoformat:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Time(hour=12, minute=34, second=56), "12:34:56", id="12:34:56"),
            pytest.param(Time(hour=12, minute=34, second=56), "12:34:56Z", id="12:34:56Z"),
            pytest.param(Time(hour=12, minute=34, second=56), "12:34:56-00:00", id="12:34:56-00:00"),
            pytest.param(Time(hour=12, minute=34, second=56), "12:34:56+00:00", id="12:34:56+00:00"),
            pytest.param(Time(hour=12, minute=34, second=56, millisecond=789), "12:34:56.789", id="12:34:56.789"),
            pytest.param(Time(hour=12, minute=34, second=56, millisecond=789), "12:34:56.789Z", id="12:34:56.789Z"),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789), "12:34:56.789-00:00", id="12:34:56.789-00:00"
            ),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789), "12:34:56.789+00:00", id="12:34:56.789+00:00"
            ),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=-13, minutes=26)),
                "12:34:56.789-12:34",
                id="12:34:56.789-12:34",
            ),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=12, minutes=34)),
                "12:34:56.789+12:34",
                id="12:34:56.789+12:34",
            ),
        ],
    )
    def test_should_accept_valid_value(self, data_type: Time, value: str):
        # Create from ISO format
        assert Time.from_isoformat(value) == data_type

    def test_should_raise_on_invalid_value(self):
        # Create from ISO format
        with pytest.raises(
            ValueError, match=re.escape("Expected ISO 8601 time with format 'hh:mm:ss.sss±hh:mm', received 'invalid'.")
        ):
            Time.from_isoformat("invalid")


class TestToIsoformat:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Time(hour=12, minute=34, second=56), "12:34:56.000Z", id="12:34:56.000Z"),
            pytest.param(Time(hour=12, minute=34, second=56, millisecond=789), "12:34:56.789Z", id="12:34:56.789Z"),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=-13, minutes=26)),
                "12:34:56.789-12:34",
                id="12:34:56.789-12:34",
            ),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=12, minutes=34)),
                "12:34:56.789+12:34",
                id="12:34:56.789+12:34",
            ),
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
        data_type = await Time.from_native(context)

        # Assert that the method returns the correct value
        assert data_type == Time()

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: Time, native: datetime.time):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Time.from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_raise_on_invalid_type(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected time of type 'datetime.time', received 'str'.")):
            await Time.from_native(context, typing.cast(datetime.time, "invalid"))


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Time, native: datetime.time):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_hour_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected hour of type 'int', received 'str'.")):
            await Time(hour=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_hour_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Hour must be between 0 and 23, received '24'.")):
            await Time(hour=24).to_native(context)

    async def test_should_raise_on_invalid_minute_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected minute of type 'int', received 'str'.")):
            await Time(minute=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_minute_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Minute must be between 0 and 59, received '60'.")):
            await Time(minute=60).to_native(context)

    async def test_should_raise_on_invalid_second_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected second of type 'int', received 'str'.")):
            await Time(second=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_second_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Second must be between 0 and 59, received '60'.")):
            await Time(second=60).to_native(context)

    async def test_should_raise_on_invalid_millisecond_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected millisecond of type 'int', received 'str'.")):
            await Time(millisecond=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_millisecond_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Millisecond must be between 0 and 999, received '1000'.")):
            await Time(millisecond=1000).to_native(context)

    async def test_should_raise_on_invalid_hours_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected hours of type 'int', received 'str'.")):
            await Time(timezone=Timezone(hours=typing.cast(int, ""))).to_native(context)

    async def test_should_raise_on_invalid_hours_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Timezone hours must be between -14 and 14, received '-15'.")):
            await Time(timezone=Timezone(hours=-15)).to_native(context)

    async def test_should_raise_on_invalid_minutes_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected minutes of type 'int', received 'str'.")):
            await Time(timezone=Timezone(minutes=typing.cast(int, ""))).to_native(context)

    async def test_should_raise_on_invalid_minutes_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Timezone minutes must be between 0 and 59, received '60'.")):
            await Time(timezone=Timezone(minutes=60)).to_native(context)


class TestDecode:
    async def test_should_raise_on_empty_buffer(self):
        # Decode data type
        with pytest.raises(DecodeError, match=re.escape("Missing field 'timezone' in message 'Time'.")):
            Time.decode(b"")

    @pytest.mark.parametrize(("data_type", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Time, buffer: bytes):
        # Decode data type
        message = Time.decode(buffer)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = Time.decode(b"\x22\x00\x08\x01\x08\x00")

        # Assert that the method returns the correct value
        assert message == Time(second=0)

    async def test_should_decode_limited_buffer(self):
        # Decode data type
        message = Time.decode(b"\x22\x00\x08\x01\x08\x00", 4)

        # Assert that the method returns the correct value
        assert message == Time(second=1)


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Time().encode()

        # Assert that the method returns the correct value
        assert message == b"\x22\x00"

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Time, buffer: bytes):
        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x02\x22\x00", id="default"),
            pytest.param(2, b"\x12\x02\x22\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode data type
        data_type = Time()
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Serialize
        xml = Serializer.serialize(Time.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<DataType><Basic>Time</Basic></DataType>"

    async def test_should_deserialize_multiline_xml(self):
        # Serialize
        xml = Serializer.serialize(Time.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Basic>Time</Basic>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Basic>Time</Basic>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, Time.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Time

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Basic>
            Time
        </Basic>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Time.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Time

    async def test_should_raise_on_unknown_basic_type(self):
        # Create xml
        xml = "<Basic>Complex</Basic>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, Time.deserialize)


class TestStringify:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Time(hour=12, minute=34, second=56), "12:34:56.000Z", id="12:34:56.000Z"),
            pytest.param(Time(hour=12, minute=34, second=56, millisecond=789), "12:34:56.789Z", id="12:34:56.789Z"),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=-13, minutes=26)),
                "12:34:56.789-12:34",
                id="12:34:56.789-12:34",
            ),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=12, minutes=34)),
                "12:34:56.789+12:34",
                id="12:34:56.789+12:34",
            ),
        ],
    )
    def test_should_return_string(self, data_type: Time, value: str):
        # Convert data type
        assert f"{data_type}" == value


class TestEquality:
    @pytest.mark.parametrize(
        ("hour", "minute", "second", "millisecond", "hours", "minutes"),
        [
            pytest.param(0, 0, 0, 0, 0, 0, id="00:00:00.000"),
            pytest.param(12, 34, 56, 789, 0, 0, id="12:34:56.789"),
            pytest.param(12, 34, 56, 789, -13, 26, id="12:34:56.789-12:34"),
            pytest.param(12, 34, 56, 789, 12, 34, id="12:34:56.789+12:34"),
        ],
    )
    def test_should_compare_equality(
        self, hour: int, minute: int, second: int, millisecond: int, hours: int, minutes: int
    ):
        assert Time(hour, minute, second, millisecond, timezone=Timezone(hours=hours, minutes=minutes)) == Time(
            hour, minute, second, millisecond, timezone=Timezone(hours=hours, minutes=minutes)
        )

    def test_shotest_should_compare_inequality(self):
        assert Time(hour=12, minute=34, second=56, millisecond=789) != object()


class TestOrder:
    @pytest.mark.parametrize(
        ("data_type_0", "data_type_1", "lt", "le", "gt", "ge"),
        [
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789),
                Time(hour=12, minute=34, second=56, millisecond=789),
                False,
                True,
                False,
                True,
                id="12:34:56.789|12:34:56.789",
            ),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789),
                Time(hour=12, minute=35, second=56, millisecond=789, timezone=Timezone(minutes=1)),
                False,
                True,
                False,
                True,
                id="12:34:56.789|12:35:56.789+00:01",
            ),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789),
                Time(hour=12, minute=33, second=56, millisecond=789, timezone=Timezone(hours=-1, minutes=59)),
                False,
                True,
                False,
                True,
                id="12:34:56.789|12:35:56.789+00:01",
            ),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=-13, minutes=26)),
                Time(hour=12, minute=34, second=56, millisecond=789),
                False,
                False,
                True,
                True,
                id="12:34:56.789-12:34|12:34:56.789",
            ),
            pytest.param(
                Time(hour=12, minute=34, second=56, millisecond=789, timezone=Timezone(hours=12, minutes=34)),
                Time(hour=12, minute=34, second=56, millisecond=789),
                True,
                True,
                False,
                False,
                id="12:34:56.789+12:34|12:34:56.789",
            ),
        ],
    )
    def test_should_order_time(self, data_type_0: Time, data_type_1: Time, lt: bool, le: bool, gt: bool, ge: bool):
        assert (data_type_0 < data_type_1) is lt
        assert (data_type_0 <= data_type_1) is le
        assert (data_type_0 > data_type_1) is gt
        assert (data_type_0 >= data_type_1) is ge

    def test_should_ignore_comparison_to_object(self):
        with pytest.raises(TypeError):
            assert (Time(hour=12, minute=34, second=56, millisecond=789) < object()) is False

        with pytest.raises(TypeError):
            assert (Time(hour=12, minute=34, second=56, millisecond=789) <= object()) is False

        with pytest.raises(TypeError):
            assert (Time(hour=12, minute=34, second=56, millisecond=789) > object()) is False

        with pytest.raises(TypeError):
            assert (Time(hour=12, minute=34, second=56, millisecond=789) >= object()) is False


class TestHash:
    def test_should_hash_constrained(self):
        # Create data type
        data_type_0 = Time(hour=12, minute=34, second=56, millisecond=789)
        data_type_1 = Time(hour=12, minute=34, second=56, millisecond=789)

        # Hash data type
        assert hash(data_type_0) == hash(data_type_1)
