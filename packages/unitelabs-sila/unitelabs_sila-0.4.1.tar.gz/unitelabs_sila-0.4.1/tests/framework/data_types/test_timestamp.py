import re
import textwrap
import unittest.mock

import pytest
import typing_extensions as typing

from sila import datetime
from sila.framework.data_types.timestamp import Timestamp
from sila.framework.data_types.timezone import Timezone
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer
from sila.framework.protobuf.decode_error import DecodeError

NATIVE_TEST_CASES = [
    pytest.param(
        Timestamp(year=1, month=1, day=1),
        datetime.datetime(year=1, month=1, day=1, tzinfo=datetime.timezone.utc),
        id="0001-01-01T00:00:00.000Z",
    ),
    pytest.param(
        Timestamp(
            year=2022,
            month=8,
            day=5,
            hour=12,
            minute=34,
            second=56,
            millisecond=789,
            timezone=Timezone(hours=12, minutes=34),
        ),
        datetime.datetime(
            year=2022,
            month=8,
            day=5,
            hour=12,
            minute=34,
            second=56,
            microsecond=789000,
            tzinfo=datetime.timezone(datetime.timedelta(hours=12, minutes=34)),
        ),
        id="2022-08-05T12:34:56.789+12:34",
    ),
]
ENCODE_TEST_CASES = [
    pytest.param(
        Timestamp(
            year=2022,
            month=8,
            day=5,
            hour=12,
            minute=34,
            second=56,
            millisecond=789,
            timezone=Timezone(hours=12, minutes=34),
        ),
        b"\x08\x38\x10\x22\x18\x0c\x20\x05\x28\x08\x30\xe6\x0f\x3a\x04\x08\x0c\x10\x22\x40\x95\x06",
        id="1: 56, 2: 34, 3: 12, 4: 5, 5: 8, 6: 2022, 7: { 1: 12, 2: 34 }, 8: 789",
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(Timestamp(), b"\x3a\x00\x48\x00", id="7: {}, 9: 0"),
    pytest.param(
        Timestamp(
            year=2022,
            month=8,
            day=5,
            hour=12,
            minute=34,
            second=56,
            millisecond=789,
            timezone=Timezone(hours=12, minutes=34),
        ),
        b"\x30\xe6\x0f\x28\x08\x20\x05\x18\x0c\x10\x22\x08\x38\x40\x95\x06\x3a\x04\x08\x0c\x10\x22\x48\x00",
        id="6: 2022, 5: 8, 4: 5, 3: 12, 2: 34, 1: 56, 8: 789, 7: { 1: 12, 2: 34 }, 9: 0",
    ),
    pytest.param(
        Timestamp(
            year=2022,
            month=8,
            day=5,
            hour=12,
            minute=34,
            second=56,
            millisecond=789,
            timezone=Timezone(hours=12, minutes=34),
        ),
        b"\x48\x00\x30\xe6\x0f\x28\x08\x20\x05\x18\x0c\x10\x22\x08\x38\x40\x95\x06\x3a\x04\x08\x0c\x10\x22",
        id="9: 0, 6: 2022, 5: 8, 4: 5, 3: 12, 2: 34, 1: 56, 8: 789, 7: { 1: 12, 2: 34 }",
    ),
]


class TestTimestamp:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Timestamp(year=1, month=1, day=1), -62_135_596_800, id="0001-01-01T00:00:00.000"),
            pytest.param(Timestamp(year=2022, month=8, day=5), 1_659_657_600, id="2022-08-05T00:00:00.000"),
            pytest.param(
                Timestamp(year=2022, month=8, day=5, timezone=Timezone(hours=14)),
                1_659_607_200,
                id="2022-08-05T00:00:00.000+14:00",
            ),
            pytest.param(
                Timestamp(year=2022, month=8, day=5, timezone=Timezone(hours=-14)),
                1_659_708_000,
                id="2022-08-05T00:00:00.000-14:00",
            ),
            pytest.param(
                Timestamp(year=2022, month=8, day=5, hour=23, minute=59, second=59, millisecond=999),
                1_659_743_999.999,
                id="2022-08-05T23:59:59.999",
            ),
            pytest.param(
                Timestamp(
                    year=2022,
                    month=8,
                    day=5,
                    hour=23,
                    minute=59,
                    second=59,
                    millisecond=999,
                    timezone=Timezone(hours=-14),
                ),
                1_659_794_399.999,
                id="2022-08-05T23:59:59.999-14:00",
            ),
            pytest.param(
                Timestamp(
                    year=2022,
                    month=8,
                    day=5,
                    hour=23,
                    minute=59,
                    second=59,
                    millisecond=999,
                    timezone=Timezone(hours=14),
                ),
                1_659_693_599.999,
                id="2022-08-05T23:59:59.999+14:00",
            ),
        ],
    )
    def test_should_convert_to_timestamp(self, data_type: Timestamp, value: int):
        # Convert data type
        assert data_type.timestamp == value


class TestInitFromIsoformat:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(
                Timestamp(year=1970, month=1, day=1, hour=12, minute=34, second=56),
                "1970-01-01T12:34:56",
                id="1970-01-01T12:34:56",
            ),
            pytest.param(
                Timestamp(year=1970, month=1, day=1, hour=12, minute=34, second=56),
                "1970-01-01T12:34:56Z",
                id="1970-01-01T12:34:56Z",
            ),
            pytest.param(
                Timestamp(year=1970, month=1, day=1, hour=12, minute=34, second=56),
                "1970-01-01T12:34:56-00:00",
                id="1970-01-01T12:34:56-00:00",
            ),
            pytest.param(
                Timestamp(year=1970, month=1, day=1, hour=12, minute=34, second=56),
                "1970-01-01T12:34:56+00:00",
                id="1970-01-01T12:34:56+00:00",
            ),
            pytest.param(
                Timestamp(year=1970, month=1, day=1, hour=12, minute=34, second=56, millisecond=789),
                "1970-01-01T12:34:56.789",
                id="1970-01-01T12:34:56.789",
            ),
            pytest.param(
                Timestamp(year=1970, month=1, day=1, hour=12, minute=34, second=56, millisecond=789),
                "1970-01-01T12:34:56.789Z",
                id="1970-01-01T12:34:56.789Z",
            ),
            pytest.param(
                Timestamp(year=1970, month=1, day=1, hour=12, minute=34, second=56, millisecond=789),
                "1970-01-01T12:34:56.789-00:00",
                id="1970-01-01T12:34:56.789-00:00",
            ),
            pytest.param(
                Timestamp(year=1970, month=1, day=1, hour=12, minute=34, second=56, millisecond=789),
                "1970-01-01T12:34:56.789+00:00",
                id="1970-01-01T12:34:56.789+00:00",
            ),
            pytest.param(
                Timestamp(
                    year=1970,
                    month=1,
                    day=1,
                    hour=12,
                    minute=34,
                    second=56,
                    millisecond=789,
                    timezone=Timezone(hours=-13, minutes=26),
                ),
                "1970-01-01T12:34:56.789-12:34",
                id="1970-01-01T12:34:56.789-12:34",
            ),
            pytest.param(
                Timestamp(
                    year=1970,
                    month=1,
                    day=1,
                    hour=12,
                    minute=34,
                    second=56,
                    millisecond=789,
                    timezone=Timezone(hours=12, minutes=34),
                ),
                "1970-01-01T12:34:56.789+12:34",
                id="1970-01-01T12:34:56.789+12:34",
            ),
        ],
    )
    def test_should_accept_valid_isoformat(self, data_type: Timestamp, value: str):
        # Create from ISO format
        assert Timestamp.from_isoformat(value) == data_type

    def test_should_raise_on_invalid_value(self):
        # Create from ISO format
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Expected ISO 8601 Timestamp with format 'YYYY-MM-DDThh:mm:ss.sss±hh:mm', received 'invalid'."
            ),
        ):
            Timestamp.from_isoformat("invalid")


class TestToIsoformat:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(
                Timestamp(year=1970, month=1, day=1, hour=12, minute=34, second=56),
                "1970-01-01T12:34:56.000Z",
                id="1970-01-01T12:34:56.000Z",
            ),
            pytest.param(
                Timestamp(year=1970, month=1, day=1, hour=12, minute=34, second=56, millisecond=789),
                "1970-01-01T12:34:56.789Z",
                id="1970-01-01T12:34:56.789Z",
            ),
            pytest.param(
                Timestamp(
                    year=1970,
                    month=1,
                    day=1,
                    hour=12,
                    minute=34,
                    second=56,
                    millisecond=789,
                    timezone=Timezone(hours=-13, minutes=26),
                ),
                "1970-01-01T12:34:56.789-12:34",
                id="1970-01-01T12:34:56.789-12:34",
            ),
            pytest.param(
                Timestamp(
                    year=1970,
                    month=1,
                    day=1,
                    hour=12,
                    minute=34,
                    second=56,
                    millisecond=789,
                    timezone=Timezone(hours=12, minutes=34),
                ),
                "1970-01-01T12:34:56.789+12:34",
                id="1970-01-01T12:34:56.789+12:34",
            ),
        ],
    )
    def test_should_convert_to_isoformat(self, data_type: Timezone, value: str):
        # Convert to ISO format
        assert data_type.to_isoformat() == value


class TestInitFromNative:
    async def test_should_raise_no_value(self):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        with pytest.raises(ValueError):
            await Timestamp.from_native(context)

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: Timestamp, native: datetime.datetime):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Timestamp.from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_raise_on_invalid_type(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(
            TypeError, match=re.escape("Expected timestamp of type 'datetime.datetime', received 'str'.")
        ):
            await Timestamp.from_native(context, typing.cast(datetime.datetime, "invalid"))


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Timestamp, native: datetime.datetime):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_year_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected year of type 'int', received 'str'.")):
            await Timestamp(year=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_year_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Year must be between 1 and 9999, received '0'.")):
            await Timestamp().to_native(context)

    async def test_should_raise_on_invalid_month_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected month of type 'int', received 'str'.")):
            await Timestamp(year=1, month=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_month_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Month must be between 1 and 12, received '0'.")):
            await Timestamp(year=1).to_native(context)

    async def test_should_raise_on_invalid_day_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected day of type 'int', received 'str'.")):
            await Timestamp(year=1, month=1, day=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_day_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Day must be between 1 and 31, received '0'.")):
            await Timestamp(year=1, month=1).to_native(context)

    async def test_should_raise_on_invalid_hour_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected hour of type 'int', received 'str'.")):
            await Timestamp(year=1, month=1, day=1, hour=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_hour_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Hour must be between 0 and 23, received '24'.")):
            await Timestamp(year=1, month=1, day=1, hour=24).to_native(context)

    async def test_should_raise_on_invalid_minute_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected minute of type 'int', received 'str'.")):
            await Timestamp(year=1, month=1, day=1, minute=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_minute_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Minute must be between 0 and 59, received '60'.")):
            await Timestamp(year=1, month=1, day=1, minute=60).to_native(context)

    async def test_should_raise_on_invalid_second_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected second of type 'int', received 'str'.")):
            await Timestamp(year=1, month=1, day=1, second=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_second_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Second must be between 0 and 59, received '60'.")):
            await Timestamp(year=1, month=1, day=1, second=60).to_native(context)

    async def test_should_raise_on_invalid_millisecond_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected millisecond of type 'int', received 'str'.")):
            await Timestamp(year=1, month=1, day=1, millisecond=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_millisecond_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Millisecond must be between 0 and 999, received '1000'.")):
            await Timestamp(year=1, month=1, day=1, millisecond=1000).to_native(context)

    async def test_should_raise_on_invalid_hours_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected hours of type 'int', received 'str'.")):
            await Timestamp(year=1, month=1, day=1, timezone=Timezone(hours=typing.cast(int, ""))).to_native(context)

    async def test_should_raise_on_invalid_hours_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Timezone hours must be between -14 and 14, received '-15'.")):
            await Timestamp(year=1, month=1, day=1, timezone=Timezone(hours=-15)).to_native(context)

    async def test_should_raise_on_invalid_minutes_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected minutes of type 'int', received 'str'.")):
            await Timestamp(year=1, month=1, day=1, timezone=Timezone(minutes=typing.cast(int, ""))).to_native(context)

    async def test_should_raise_on_invalid_minutes_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Timezone minutes must be between 0 and 59, received '60'.")):
            await Timestamp(year=1, month=1, day=1, timezone=Timezone(minutes=60)).to_native(context)


class TestDecode:
    async def test_should_raise_on_empty_buffer(self):
        # Decode data type
        with pytest.raises(DecodeError, match=re.escape("Missing field 'timezone' in message 'Timestamp'.")):
            Timestamp.decode(b"")

    @pytest.mark.parametrize(("data_type", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Timestamp, buffer: bytes):
        # Decode data type
        message = Timestamp.decode(buffer)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = Timestamp.decode(b"\x3a\x00\x30\x01\x30\x00")

        # Assert that the method returns the correct value
        assert message == Timestamp(year=0)

    async def test_should_decode_limited_buffer(self):
        # Decode data type
        message = Timestamp.decode(b"\x3a\x00\x30\x01\x30\x00", 4)

        # Assert that the method returns the correct value
        assert message == Timestamp(year=1)


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Timestamp().encode()

        # Assert that the method returns the correct value
        assert message == b"\x3a\x00"

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Timestamp, buffer: bytes):
        # Encode data type
        message = data_type.encode()

        # Assert that the method returns the correct value
        assert message == buffer

    @pytest.mark.parametrize(
        ("number", "buffer"),
        [
            pytest.param(1, b"\x0a\x02\x3a\x00", id="default"),
            pytest.param(2, b"\x12\x02\x3a\x00", id="custom"),
        ],
    )
    async def test_should_encode_field_number(self, number: int, buffer: bytes):
        # Encode data type
        data_type = Timestamp()
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Serialize
        xml = Serializer.serialize(Timestamp.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<DataType><Basic>Timestamp</Basic></DataType>"

    async def test_should_deserialize_multiline_xml(self):
        # Serialize
        xml = Serializer.serialize(Timestamp.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Basic>Timestamp</Basic>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Basic>Timestamp</Basic>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, Timestamp.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Timestamp

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Basic>
            Timestamp
        </Basic>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Timestamp.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Timestamp

    async def test_should_raise_on_unknown_basic_type(self):
        # Create xml
        xml = "<Basic>Complex</Basic>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, Timestamp.deserialize)


class TestStringify:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(
                Timestamp(year=2022, month=8, day=5, hour=12, minute=34, second=56, millisecond=789),
                "2022-08-05T12:34:56.789Z",
                id="2022-08-05T12:34:56.789Z",
            ),
            pytest.param(
                Timestamp(
                    year=2022,
                    month=8,
                    day=5,
                    hour=12,
                    minute=34,
                    second=56,
                    millisecond=789,
                    timezone=Timezone(hours=-13, minutes=26),
                ),
                "2022-08-05T12:34:56.789-12:34",
                id="2022-08-05T12:34:56.789-12:34",
            ),
            pytest.param(
                Timestamp(
                    year=2022,
                    month=8,
                    day=5,
                    hour=12,
                    minute=34,
                    second=56,
                    millisecond=789,
                    timezone=Timezone(hours=12, minutes=34),
                ),
                "2022-08-05T12:34:56.789+12:34",
                id="2022-08-05T12:34:56.789+12:34",
            ),
        ],
    )
    def test_should_return_string(self, data_type: Timestamp, value: str):
        # Convert data type
        assert f"{data_type}" == value


class TestEquality:
    @pytest.mark.parametrize(
        ("year", "month", "day", "hour", "minute", "second", "millisecond", "hours", "minutes"),
        [
            pytest.param(2022, 8, 5, 0, 0, 0, 0, 0, 0, id="2022-08-05T00:00:00.000"),
            pytest.param(2022, 8, 5, 12, 34, 56, 789, 0, 0, id="2022-08-05T12:34:56.789"),
            pytest.param(2022, 8, 5, 12, 34, 56, 789, -12, 34, id="2022-08-05T12:34:56.789-12:34"),
            pytest.param(2022, 8, 5, 12, 34, 56, 789, 12, 34, id="2022-08-05T12:34:56.789+12:34"),
        ],
    )
    def test_should_compare_equality(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        millisecond: int,
        hours: int,
        minutes: int,
    ):
        assert Timestamp(
            year, month, day, hour, minute, second, millisecond, timezone=Timezone(hours=hours, minutes=minutes)
        ) == Timestamp(
            year, month, day, hour, minute, second, millisecond, timezone=Timezone(hours=hours, minutes=minutes)
        )

    def test_should_compare_inequality(self):
        assert Timestamp(hour=12, minute=34, second=56, millisecond=789) != object()


class TestOrder:
    @pytest.mark.parametrize(
        ("data_type_0", "data_type_1", "lt", "le", "gt", "ge"),
        [
            pytest.param(
                Timestamp(year=2022, month=8, day=5, hour=12, minute=34, second=56, millisecond=789),
                Timestamp(year=2022, month=8, day=5, hour=12, minute=34, second=56, millisecond=789),
                False,
                True,
                False,
                True,
                id="2022-08-05T12:34:56.789|2022-08-05T12:34:56.789",
            ),
            pytest.param(
                Timestamp(year=2022, month=8, day=5, hour=12, minute=34, second=56, millisecond=789),
                Timestamp(
                    year=2022,
                    month=8,
                    day=5,
                    hour=12,
                    minute=35,
                    second=56,
                    millisecond=789,
                    timezone=Timezone(minutes=1),
                ),
                False,
                True,
                False,
                True,
                id="2022-08-05T12:34:56.789|2022-08-05T12:35:56.789+00:01",
            ),
            pytest.param(
                Timestamp(year=2022, month=8, day=5, hour=12, minute=34, second=56, millisecond=789),
                Timestamp(
                    year=2022,
                    month=8,
                    day=5,
                    hour=12,
                    minute=33,
                    second=56,
                    millisecond=789,
                    timezone=Timezone(hours=-1, minutes=59),
                ),
                False,
                True,
                False,
                True,
                id="2022-08-05T12:34:56.789|2022-08-05T12:35:56.789+00:01",
            ),
            pytest.param(
                Timestamp(
                    year=2022,
                    month=8,
                    day=5,
                    hour=12,
                    minute=34,
                    second=56,
                    millisecond=789,
                    timezone=Timezone(hours=-13, minutes=26),
                ),
                Timestamp(year=2022, month=8, day=5, hour=12, minute=34, second=56, millisecond=789),
                False,
                False,
                True,
                True,
                id="2022-08-05T12:34:56.789-12:34|2022-08-05T12:34:56.789",
            ),
            pytest.param(
                Timestamp(
                    year=2022,
                    month=8,
                    day=5,
                    hour=12,
                    minute=34,
                    second=56,
                    millisecond=789,
                    timezone=Timezone(hours=12, minutes=34),
                ),
                Timestamp(year=2022, month=8, day=5, hour=12, minute=34, second=56, millisecond=789),
                True,
                True,
                False,
                False,
                id="2022-08-05T12:34:56.789+12:34|2022-08-05T12:34:56.789",
            ),
        ],
    )
    def test_should_order_timestamp(
        self, data_type_0: Timestamp, data_type_1: Timestamp, lt: bool, le: bool, gt: bool, ge: bool
    ):
        assert (data_type_0 < data_type_1) is lt
        assert (data_type_0 <= data_type_1) is le
        assert (data_type_0 > data_type_1) is gt
        assert (data_type_0 >= data_type_1) is ge

    def test_should_ignore_comparison_to_object(self):
        with pytest.raises(TypeError):
            assert (Timestamp(hour=12, minute=34, second=56, millisecond=789) < object()) is False

        with pytest.raises(TypeError):
            assert (Timestamp(hour=12, minute=34, second=56, millisecond=789) <= object()) is False

        with pytest.raises(TypeError):
            assert (Timestamp(hour=12, minute=34, second=56, millisecond=789) > object()) is False

        with pytest.raises(TypeError):
            assert (Timestamp(hour=12, minute=34, second=56, millisecond=789) >= object()) is False


class TestHash:
    def test_should_hash_constrained(self):
        # Create data type
        data_type_0 = Timestamp(year=2022, month=8, day=5, hour=12, minute=34, second=56, millisecond=789)
        data_type_1 = Timestamp(year=2022, month=8, day=5, hour=12, minute=34, second=56, millisecond=789)

        # Hash data type
        assert hash(data_type_0) == hash(data_type_1)
