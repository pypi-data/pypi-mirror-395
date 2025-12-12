import re
import textwrap
import unittest.mock

import pytest
import typing_extensions as typing

from sila import datetime
from sila.framework.data_types.date import Date
from sila.framework.data_types.timezone import Timezone
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer
from sila.framework.protobuf.decode_error import DecodeError

NATIVE_TEST_CASES = [
    pytest.param(Date(year=1, month=1, day=1), datetime.date.min, id="0001-01-01"),
    pytest.param(Date(year=2022, month=8, day=5), datetime.date(year=2022, month=8, day=5), id="2022-08-05"),
    pytest.param(Date(year=9999, month=12, day=31), datetime.date.max, id="9999-12-31"),
    pytest.param(
        Date(year=2022, month=8, day=5),
        datetime.date(year=2022, month=8, day=5, tzinfo=datetime.timezone.utc),
        id="2022-08-05Z",
    ),
    pytest.param(
        Date(year=1, month=1, day=1, timezone=Timezone(hours=12, minutes=34)),
        datetime.date(year=1, month=1, day=1, tzinfo=datetime.timezone(datetime.timedelta(hours=12, minutes=34))),
        id="0001-01-01+12:34",
    ),
    pytest.param(
        Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)),
        datetime.date(year=2022, month=8, day=5, tzinfo=datetime.timezone(datetime.timedelta(hours=12, minutes=34))),
        id="2022-08-05+12:34",
    ),
    pytest.param(
        Date(year=9999, month=12, day=31, timezone=Timezone(hours=12, minutes=34)),
        datetime.date(year=9999, month=12, day=31, tzinfo=datetime.timezone(datetime.timedelta(hours=12, minutes=34))),
        id="9999-12-31+12:34",
    ),
]
ENCODE_TEST_CASES = [
    pytest.param(
        Date(year=1, month=1, day=1, timezone=Timezone(hours=-12)),
        b"\x08\x01\x10\x01\x18\x01\x22\x0b\x08\xf4\xff\xff\xff\xff\xff\xff\xff\xff\x01",
        id="1: 1, 2: 1, 3: 1, 4: { 1: -12 }",
    ),
    pytest.param(
        Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)),
        b"\x08\x05\x10\x08\x18\xe6\x0f\x22\x04\x08\x0c\x10\x22",
        id="1: 5, 2: 8, 3: 2022, 4: { 1: 12, 2: 34 }",
    ),
    pytest.param(
        Date(year=9999, month=12, day=31),
        b"\x08\x1f\x10\x0c\x18\x8f\x4e\x22\x00",
        id="1: 31, 2: 12, 3: 9999",
    ),
]
DECODE_TEST_CASES = [
    *ENCODE_TEST_CASES,
    pytest.param(Date(), b"\x22\x00\x28\x00", id="4: {}, 5: 0"),
    pytest.param(
        Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)),
        b"\x18\xe6\x0f\x10\x08\x08\x05\x22\x04\x08\x0c\x10\x22\x28\x00",
        id="3: 2022, 2: 8, 1: 5, 4: { 1: 12, 2: 34 }, 5: 0",
    ),
    pytest.param(
        Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)),
        b"\x28\x00\x18\xe6\x0f\x10\x08\x08\x05\x22\x04\x08\x0c\x10\x22",
        id="5: 0, 3: 2022, 2: 8, 1: 5, 4: { 1: 12, 2: 34 }",
    ),
]


class TestTimestamp:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Date(year=1, month=1, day=1), -62_135_596_800, id="0001-01-01"),
            pytest.param(Date(year=2022, month=8, day=5), 1_659_657_600, id="2022-08-05"),
            pytest.param(
                Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)),
                1_659_612_360,
                id="2022-08-05+12:34",
            ),
            pytest.param(Date(year=9999, month=12, day=31), 253_402_214_400, id="9999-12-31"),
        ],
    )
    def test_should_convert_to_timestamp(self, data_type: Date, value: int):
        # Convert data type
        assert data_type.timestamp == value


class TestInitFromIsoformat:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Date(year=2022, month=8, day=5), "2022-08-05", id="2022-08-05"),
            pytest.param(Date(year=2022, month=8, day=5), "2022-08-05Z", id="2022-08-05Z"),
            pytest.param(Date(year=2022, month=8, day=5), "2022-08-05+00:00", id="2022-08-05+00:00"),
            pytest.param(
                Date(year=2022, month=8, day=5, timezone=Timezone(hours=-13, minutes=26)),
                "2022-08-05-12:34",
                id="2022-08-05-12:34",
            ),
            pytest.param(
                Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)),
                "2022-08-05+12:34",
                id="2022-08-05+12:34",
            ),
        ],
    )
    def test_should_accept_valid_value(self, data_type: Date, value: str):
        # Create from ISO format
        assert Date.from_isoformat(value) == data_type

    def test_should_raise_on_invalid_value(self):
        # Create from ISO format
        with pytest.raises(
            ValueError, match=re.escape("Expected ISO 8601 date with format 'YYYY-MM-DD±hh:mm', received 'invalid'.")
        ):
            Date.from_isoformat("invalid")


class TestToIsoformat:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            pytest.param(Date(year=2022, month=8, day=5), "2022-08-05Z", id="2022-08-05Z"),
            pytest.param(
                Date(year=2022, month=8, day=5, timezone=Timezone(hours=-13, minutes=26)),
                "2022-08-05-12:34",
                id="2022-08-05-12:34",
            ),
            pytest.param(
                Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)),
                "2022-08-05+12:34",
                id="2022-08-05+12:34",
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
            await Date.from_native(context)

    @pytest.mark.parametrize(("expected", "native"), NATIVE_TEST_CASES)
    async def test_should_accept_native(self, expected: Date, native: datetime.date):
        # Create context
        context = unittest.mock.Mock()

        # Initialize from native
        data_type = await Date.from_native(context, native)

        # Assert that the method returns the correct value
        assert data_type == expected

    async def test_should_raise_on_invalid_type(self):
        # Convert data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected date of type 'datetime.date', received 'str'.")):
            await Date.from_native(context, typing.cast(datetime.date, "invalid"))


class TestConvertToNative:
    @pytest.mark.parametrize(("data_type", "native"), NATIVE_TEST_CASES)
    async def test_should_convert_to_native(self, data_type: Date, native: datetime.date):
        # Convert data type
        context = unittest.mock.Mock()
        assert await data_type.to_native(context) == native

    async def test_should_raise_on_invalid_year_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected year of type 'int', received 'str'.")):
            await Date(year=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_year_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Year must be between 1 and 9999, received '0'.")):
            await Date().to_native(context)

    async def test_should_raise_on_invalid_month_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected month of type 'int', received 'str'.")):
            await Date(year=1, month=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_month_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Month must be between 1 and 12, received '0'.")):
            await Date(year=1).to_native(context)

    async def test_should_raise_on_invalid_day_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected day of type 'int', received 'str'.")):
            await Date(year=1, month=1, day=typing.cast(int, "")).to_native(context)

    async def test_should_raise_on_invalid_day_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Day must be between 1 and 31, received '0'.")):
            await Date(year=1, month=1).to_native(context)

    async def test_should_raise_on_invalid_hours_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected hours of type 'int', received 'str'.")):
            await Date(year=1, month=1, day=1, timezone=Timezone(hours=typing.cast(int, ""))).to_native(context)

    async def test_should_raise_on_invalid_hours_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Timezone hours must be between -14 and 14, received '-15'.")):
            await Date(year=1, month=1, day=1, timezone=Timezone(hours=-15)).to_native(context)

    async def test_should_raise_on_invalid_minutes_type(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(TypeError, match=re.escape("Expected minutes of type 'int', received 'str'.")):
            await Date(year=1, month=1, day=1, timezone=Timezone(minutes=typing.cast(int, ""))).to_native(context)

    async def test_should_raise_on_invalid_minutes_value(self):
        # Create data type
        context = unittest.mock.Mock()

        with pytest.raises(ValueError, match=re.escape("Timezone minutes must be between 0 and 59, received '60'.")):
            await Date(year=1, month=1, day=1, timezone=Timezone(minutes=60)).to_native(context)


class TestDecode:
    async def test_should_raise_on_empty_buffer(self):
        # Decode data type
        with pytest.raises(DecodeError, match=re.escape("Missing field 'timezone' in message 'Date'.")):
            Date.decode(b"")

    @pytest.mark.parametrize(("data_type", "buffer"), DECODE_TEST_CASES)
    async def test_should_decode_custom_buffer(self, data_type: Date, buffer: bytes):
        # Decode data type
        message = Date.decode(buffer)

        # Assert that the method returns the correct value
        assert message == data_type

    async def test_should_decode_multiple_fields(self):
        # Decode message
        message = Date.decode(b"\x22\x00\x18\x01\x18\x00")

        # Assert that the method returns the correct value
        assert message == Date(year=0)

    async def test_should_decode_limited_buffer(self):
        # Decode data type
        message = Date.decode(b"\x22\x00\x18\x01\x18\x00", 4)

        # Assert that the method returns the correct value
        assert message == Date(year=1)


class TestEncode:
    async def test_should_encode_default_values(self):
        # Encode data type
        message = Date().encode()

        # Assert that the method returns the correct value
        assert message == b"\x22\x00"

    @pytest.mark.parametrize(("data_type", "buffer"), ENCODE_TEST_CASES)
    async def test_should_encode_custom_values(self, data_type: Date, buffer: bytes):
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
        data_type = Date()
        message = data_type.encode(None, number)

        # Assert that the method returns the correct value
        assert message == buffer


class TestSerialize:
    async def test_should_serialize_singleline_xml(self):
        # Serialize
        xml = Serializer.serialize(Date.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == "<DataType><Basic>Date</Basic></DataType>"

    async def test_should_deserialize_multiline_xml(self):
        # Serialize
        xml = Serializer.serialize(Date.serialize)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <DataType>
              <Basic>Date</Basic>
            </DataType>
            """
        )


class TestDeserialize:
    async def test_should_deserialize_singleline_xml(self):
        # Create xml
        xml = "<Basic>Date</Basic>"

        # Deserialize
        data_type = Deserializer.deserialize(xml, Date.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Date

    async def test_should_deserialize_multiline_xml(self):
        # Create xml
        xml = """
        <Basic>
            Date
        </Basic>
        """

        # Deserialize
        data_type = Deserializer.deserialize(xml, Date.deserialize)

        # Assert that the method returns the correct value
        assert data_type == Date

    async def test_should_raise_on_unknown_basic_type(self):
        # Create xml
        xml = "<Basic>Complex</Basic>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Expected basic type value, received 'Complex'.")):
            Deserializer.deserialize(xml, Date.deserialize)


class TestStringify:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Date(year=2022, month=8, day=5), "2022-08-05Z"),
            (Date(year=2022, month=8, day=5, timezone=Timezone(hours=-13, minutes=26)), "2022-08-05-12:34"),
            (Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)), "2022-08-05+12:34"),
        ],
    )
    def test_should_return_string(self, data_type: Date, value: str):
        # Convert data type
        assert f"{data_type}" == value


class TestEquality:
    @pytest.mark.parametrize(
        ("year", "month", "day", "hours", "minutes"),
        [
            pytest.param(0, 0, 0, 0, 0, id="0000-00-00"),
            pytest.param(2022, 8, 5, 0, 0, id="2022-08-05"),
            pytest.param(2022, 8, 5, -13, 26, id="2022-08-05-12:34"),
            pytest.param(2022, 8, 5, 12, 34, id="2022-08-05+12:34"),
        ],
    )
    def test_should_compare_equality(self, year: int, month: int, day: int, hours: int, minutes: int):
        assert Date(year, month, day, timezone=Timezone(hours=hours, minutes=minutes)) == Date(
            year, month, day, timezone=Timezone(hours=hours, minutes=minutes)
        )

    def test_should_compare_inequality(self):
        assert Date(year=2022, month=8, day=5) != object()


class TestOrder:
    @pytest.mark.parametrize(
        ("data_type_0", "data_type_1", "lt", "le", "gt", "ge"),
        [
            pytest.param(
                Date(year=2022, month=8, day=5),
                Date(year=2022, month=8, day=5),
                False,
                True,
                False,
                True,
                id="2022-08-05",
            ),
            pytest.param(
                Date(year=2022, month=8, day=5, timezone=Timezone(hours=-13, minutes=26)),
                Date(year=2022, month=8, day=5),
                False,
                False,
                True,
                True,
                id="2022-08-05-12:34",
            ),
            pytest.param(
                Date(year=2022, month=8, day=5, timezone=Timezone(hours=12, minutes=34)),
                Date(year=2022, month=8, day=5),
                True,
                True,
                False,
                False,
                id="2022-08-05+12:34",
            ),
        ],
    )
    def test_should_order_date(self, data_type_0: Date, data_type_1: Date, lt: bool, le: bool, gt: bool, ge: bool):
        assert (data_type_0 < data_type_1) is lt
        assert (data_type_0 <= data_type_1) is le
        assert (data_type_0 > data_type_1) is gt
        assert (data_type_0 >= data_type_1) is ge

    def test_should_ignore_comparison_to_object(self):
        with pytest.raises(TypeError):
            assert (Date(year=2022, month=8, day=5) < object()) is False

        with pytest.raises(TypeError):
            assert (Date(year=2022, month=8, day=5) <= object()) is False

        with pytest.raises(TypeError):
            assert (Date(year=2022, month=8, day=5) > object()) is False

        with pytest.raises(TypeError):
            assert (Date(year=2022, month=8, day=5) >= object()) is False


class TestHash:
    def test_should_hash_constrained(self):
        # Create data type
        data_type_0 = Date(year=2022, month=8, day=5)
        data_type_1 = Date(year=2022, month=8, day=5)

        # Hash data type
        assert hash(data_type_0) == hash(data_type_1)
