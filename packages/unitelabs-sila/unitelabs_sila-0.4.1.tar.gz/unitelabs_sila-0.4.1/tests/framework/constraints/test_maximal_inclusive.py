import math
import re
import sys

import pytest
import typing_extensions as typing

from sila.framework.constraints.maximal_inclusive import MaximalInclusive
from sila.framework.data_types.date import Date
from sila.framework.data_types.integer import Integer
from sila.framework.data_types.real import Real
from sila.framework.data_types.string import String
from sila.framework.data_types.structure import Structure
from sila.framework.data_types.time import Time
from sila.framework.data_types.timestamp import Timestamp
from sila.framework.data_types.timezone import Timezone
from sila.framework.fdl.deserializer import Deserializer
from sila.framework.fdl.parse_error import ParseError
from sila.framework.fdl.serializer import Serializer


class TestInitialize:
    async def test_should_initialize(self):
        # Create constraint
        constraint = MaximalInclusive(Integer(0))

        # Assert that the method returns the correct value
        assert constraint.value == Integer(0)


class TestValidate:
    @pytest.mark.parametrize(("value"), [Integer(-sys.maxsize - 1), Integer(2), Integer(3)])
    async def test_should_validate_integer(self, value: Integer):
        # Create constraint
        constraint = MaximalInclusive(Integer(3))

        # Validate constraint
        assert await constraint.validate(value) is True

    async def test_should_raise_on_invalid_integer_type(self):
        # Create constraint
        constraint = MaximalInclusive(Integer(3))

        # Validate constraint
        with pytest.raises(
            TypeError,
            match=re.escape("Expected value of type 'Integer', received 'Structure'."),
        ):
            await constraint.validate(typing.cast(Integer, Structure()))

    @pytest.mark.parametrize(("value"), [Integer(4), Integer(sys.maxsize)])
    async def test_should_raise_on_invalid_integer_value(self, value: Integer):
        # Create constraint
        constraint = MaximalInclusive(Integer(3))

        # Validate constraint
        with pytest.raises(
            ValueError,
            match=re.escape(f"Value '{value}' must be less than or equal to the maximal inclusive limit of '3'."),
        ):
            await constraint.validate(value)

    @pytest.mark.parametrize(("value"), [Real(sys.float_info.min), Real(3.2), Real(3.2999999999), Real(3.3)])
    async def test_should_validate_real(self, value: Real):
        # Create constraint
        constraint = MaximalInclusive(Real(3.3))

        # Validate constraint
        assert await constraint.validate(value) is True

    async def test_should_raise_on_invalid_real_type(self):
        # Create constraint
        constraint = MaximalInclusive(Real(3.3))

        # Validate constraint
        with pytest.raises(
            TypeError,
            match=re.escape("Expected value of type 'Real', received 'Structure'."),
        ):
            await constraint.validate(typing.cast(Real, Structure()))

    @pytest.mark.parametrize(("value"), [Real(3.3000000001), Real(3.4), Real(sys.float_info.max)])
    async def test_should_raise_on_invalid_real_value(self, value: Real):
        # Create constraint
        constraint = MaximalInclusive(Real(3.3))

        # Validate constraint
        with pytest.raises(
            ValueError,
            match=re.escape(f"Value '{value}' must be less than or equal to the maximal inclusive limit of '3.3'."),
        ):
            await constraint.validate(value)

    @pytest.mark.parametrize(
        ("value"),
        [
            Date(1, 1, 1),
            Date(1970, 1, 1, Timezone(hours=2, minutes=1)),
            Date(1970, 1, 3, Timezone(hours=2)),
        ],
    )
    async def test_should_validate_date(self, value: Date):
        # Create constraint
        constraint = MaximalInclusive(Date(1970, 1, 3, Timezone(hours=2)))

        # Validate constraint
        assert await constraint.validate(value) is True

    async def test_should_raise_on_invalid_date_type(self):
        # Create constraint
        constraint = MaximalInclusive(Date(1970, 1, 3, Timezone(hours=2)))

        # Validate constraint
        with pytest.raises(
            TypeError,
            match=re.escape("Expected value of type 'Date', received 'Structure'."),
        ):
            await constraint.validate(typing.cast(Date, Structure()))

    @pytest.mark.parametrize(
        ("value"),
        [Date(1970, 1, 3, Timezone(hours=1, minutes=59)), Date(9999, 12, 31)],
    )
    async def test_should_raise_on_invalid_date_value(self, value: Date):
        # Create constraint
        constraint = MaximalInclusive(Date(1970, 1, 3, Timezone(hours=2)))

        # Validate constraint
        with pytest.raises(
            ValueError,
            match=re.escape(
                f"Value '{value}' must be less than or equal to the maximal inclusive limit of '1970-01-03+02:00'."
            ),
        ):
            await constraint.validate(value)

    @pytest.mark.parametrize(
        ("value"),
        [
            Time(),
            Time(8, 34, 56, 789, Timezone(hours=-2, minutes=1)),
            Time(9, 34, 56, 789, Timezone(hours=-1, minutes=1)),
            Time(10, 34, 56, 789, Timezone(minutes=1)),
            Time(11, 34, 56, 789, Timezone(hours=1, minutes=1)),
            Time(12, 34, 56, 789, Timezone(hours=2, minutes=1)),
            Time(8, 34, 56, 789, Timezone(hours=-2)),
            Time(9, 34, 56, 789, Timezone(hours=-1)),
            Time(10, 34, 56, 789),
            Time(11, 34, 56, 789, Timezone(hours=1)),
            Time(12, 34, 56, 789, Timezone(hours=2)),
        ],
    )
    async def test_should_validate_time(self, value: Time):
        # Create constraint
        constraint = MaximalInclusive(Time(12, 34, 56, 789, Timezone(hours=2)))

        # Validate constraint
        assert await constraint.validate(value) is True

    async def test_should_raise_on_invalid_time_type(self):
        # Create constraint
        constraint = MaximalInclusive(Time(12, 34, 56, 789, Timezone(hours=2)))

        # Validate constraint
        with pytest.raises(
            TypeError,
            match=re.escape("Expected value of type 'Time', received 'Structure'."),
        ):
            await constraint.validate(typing.cast(Time, Structure()))

    @pytest.mark.parametrize(
        ("value"),
        [
            Time(8, 34, 56, 789, Timezone(hours=-3, minutes=59)),
            Time(9, 34, 56, 789, Timezone(hours=-2, minutes=59)),
            Time(10, 34, 56, 789, Timezone(hours=-1, minutes=59)),
            Time(11, 34, 56, 789, Timezone(minutes=59)),
            Time(12, 34, 56, 789, Timezone(hours=1, minutes=59)),
            Time(23, 59, 59, 999),
        ],
    )
    async def test_should_raise_on_invalid_time_value(self, value: Time):
        # Create constraint
        constraint = MaximalInclusive(Time(12, 34, 56, 789, Timezone(hours=2)))

        # Validate constraint
        with pytest.raises(
            ValueError,
            match=re.escape(
                f"Value '{value}' must be less than or equal to the maximal inclusive limit of '12:34:56.789+02:00'."
            ),
        ):
            await constraint.validate(value)

    @pytest.mark.parametrize(
        ("value"),
        [
            Timestamp(1, 1, 1),
            Timestamp(1970, 1, 1, 8, 34, 56, 789, Timezone(hours=-2, minutes=1)),
            Timestamp(1970, 1, 1, 9, 34, 56, 789, Timezone(hours=-1, minutes=1)),
            Timestamp(1970, 1, 1, 10, 34, 56, 789, Timezone(minutes=1)),
            Timestamp(1970, 1, 1, 11, 34, 56, 789, Timezone(hours=1, minutes=1)),
            Timestamp(1970, 1, 1, 12, 34, 56, 789, Timezone(hours=2, minutes=1)),
            Timestamp(1970, 1, 1, 8, 34, 56, 789, Timezone(hours=-2)),
            Timestamp(1970, 1, 1, 9, 34, 56, 789, Timezone(hours=-1)),
            Timestamp(1970, 1, 1, 10, 34, 56, 789),
            Timestamp(1970, 1, 1, 11, 34, 56, 789, Timezone(hours=1)),
            Timestamp(1970, 1, 1, 12, 34, 56, 789, Timezone(hours=2)),
        ],
    )
    async def test_should_validate_timestamp(self, value: Timestamp):
        # Create constraint
        constraint = MaximalInclusive(Timestamp(1970, 1, 1, 12, 34, 56, 789, Timezone(hours=2)))

        # Validate constraint
        assert await constraint.validate(value) is True

    async def test_should_raise_on_invalid_timestamp_type(self):
        # Create constraint
        constraint = MaximalInclusive(Timestamp(1970, 1, 1, 12, 34, 56, 789, Timezone(hours=2)))

        # Validate constraint
        with pytest.raises(
            TypeError,
            match=re.escape("Expected value of type 'Timestamp', received 'Structure'."),
        ):
            await constraint.validate(typing.cast(Timestamp, Structure()))

    @pytest.mark.parametrize(
        ("value"),
        [
            Timestamp(1970, 1, 1, 8, 34, 56, 789, Timezone(hours=-3, minutes=59)),
            Timestamp(1970, 1, 1, 9, 34, 56, 789, Timezone(hours=-2, minutes=59)),
            Timestamp(1970, 1, 1, 10, 34, 56, 789, Timezone(hours=-1, minutes=59)),
            Timestamp(1970, 1, 1, 11, 34, 56, 789, Timezone(minutes=59)),
            Timestamp(1970, 1, 1, 12, 34, 56, 789, Timezone(hours=1, minutes=59)),
            Timestamp(9999, 12, 31, 23, 59, 59, 999),
        ],
    )
    async def test_should_raise_on_invalid_timestamp_value(self, value: Timestamp):
        # Create constraint
        constraint = MaximalInclusive(Timestamp(1970, 1, 1, 12, 34, 56, 789, Timezone(hours=2)))

        # Validate constraint
        with pytest.raises(
            ValueError,
            match=re.escape(
                f"Value '{value}' must be less than or equal to "
                "the maximal inclusive limit of '1970-01-01T12:34:56.789+02:00'."
            ),
        ):
            await constraint.validate(value)


class TestSerialize:
    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Integer(-sys.maxsize - 1), "-9223372036854775808"),
            (Integer(3), "3"),
            (Integer(sys.maxsize), "9223372036854775807"),
        ],
    )
    async def test_should_serialize_integer(self, data_type: Integer, value: str):
        # Create constraint
        constraint = MaximalInclusive(data_type)

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == f"<MaximalInclusive>{value}</MaximalInclusive>"

    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Real(sys.float_info.min), "2.2250738585072014e-308"),
            (Real(-math.pi), "-3.141592653589793"),
            (Real(3.3), "3.3"),
            (Real(math.pi), "3.141592653589793"),
            (Real(sys.float_info.max), "1.7976931348623157e+308"),
        ],
    )
    async def test_should_serialize_real(self, data_type: Real, value: str):
        # Create constraint
        constraint = MaximalInclusive(data_type)

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == f"<MaximalInclusive>{value}</MaximalInclusive>"

    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Date(1, 1, 1, timezone=Timezone(hours=-14)), "0001-01-01-14:00"),
            (Date(1, 1, 1), "0001-01-01Z"),
            (Date(1, 1, 1, timezone=Timezone(hours=14)), "0001-01-01+14:00"),
            (Date(2022, 8, 5, timezone=Timezone(hours=-3, minutes=30)), "2022-08-05-02:30"),
            (Date(2022, 8, 5), "2022-08-05Z"),
            (Date(2022, 8, 5, timezone=Timezone(hours=2, minutes=30)), "2022-08-05+02:30"),
            (Date(9999, 12, 31, timezone=Timezone(hours=-14)), "9999-12-31-14:00"),
            (Date(9999, 12, 31), "9999-12-31Z"),
            (Date(9999, 12, 31, timezone=Timezone(hours=14)), "9999-12-31+14:00"),
        ],
    )
    async def test_should_serialize_date(self, data_type: Date, value: str):
        # Create constraint
        constraint = MaximalInclusive(data_type)

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == f"<MaximalInclusive>{value}</MaximalInclusive>"

    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Time(0, 0, 0, 0, timezone=Timezone(hours=-14)), "00:00:00.000-14:00"),
            (Time(0, 0, 0, 0), "00:00:00.000Z"),
            (Time(0, 0, 0, 0, timezone=Timezone(hours=14)), "00:00:00.000+14:00"),
            (Time(12, 34, 56, 789, timezone=Timezone(hours=-3, minutes=30)), "12:34:56.789-02:30"),
            (Time(12, 34, 56, 789), "12:34:56.789Z"),
            (Time(12, 34, 56, 789, timezone=Timezone(hours=2, minutes=30)), "12:34:56.789+02:30"),
            (Time(23, 59, 59, 999, timezone=Timezone(hours=-14)), "23:59:59.999-14:00"),
            (Time(23, 59, 59, 999), "23:59:59.999Z"),
            (Time(23, 59, 59, 999, timezone=Timezone(hours=14)), "23:59:59.999+14:00"),
        ],
    )
    async def test_should_serialize_time(self, data_type: Time, value: str):
        # Create constraint
        constraint = MaximalInclusive(data_type)

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == f"<MaximalInclusive>{value}</MaximalInclusive>"

    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Timestamp(2022, 8, 5, 0, 0, 0, 0, timezone=Timezone(hours=-14)), "2022-08-05T00:00:00.000-14:00"),
            (Timestamp(2022, 8, 5, 0, 0, 0, 0), "2022-08-05T00:00:00.000Z"),
            (Timestamp(2022, 8, 5, 0, 0, 0, 0, timezone=Timezone(hours=14)), "2022-08-05T00:00:00.000+14:00"),
            (
                Timestamp(2022, 8, 5, 12, 34, 56, 789, timezone=Timezone(hours=-3, minutes=30)),
                "2022-08-05T12:34:56.789-02:30",
            ),
            (Timestamp(2022, 8, 5, 12, 34, 56, 789), "2022-08-05T12:34:56.789Z"),
            (
                Timestamp(2022, 8, 5, 12, 34, 56, 789, timezone=Timezone(hours=2, minutes=30)),
                "2022-08-05T12:34:56.789+02:30",
            ),
            (Timestamp(2022, 8, 5, 23, 59, 59, 999, timezone=Timezone(hours=-14)), "2022-08-05T23:59:59.999-14:00"),
            (Timestamp(2022, 8, 5, 23, 59, 59, 999), "2022-08-05T23:59:59.999Z"),
            (Timestamp(2022, 8, 5, 23, 59, 59, 999, timezone=Timezone(hours=14)), "2022-08-05T23:59:59.999+14:00"),
        ],
    )
    async def test_should_serialize_timestamp(self, data_type: Timestamp, value: str):
        # Create constraint
        constraint = MaximalInclusive(data_type)

        # Serialize
        xml = Serializer.serialize(constraint.serialize, remove_whitespace=True)

        # Assert that the method returns the correct value
        assert xml == f"<MaximalInclusive>{value}</MaximalInclusive>"


class TestDeserialize:
    async def test_should_raise_on_missing_data_type(self):
        # Create xml
        xml = "<MaximalInclusive>2</MaximalInclusive>"

        # Deserialize
        with pytest.raises(ParseError, match=re.escape("Missing 'data_type' in context.")):
            Deserializer.deserialize(xml, MaximalInclusive.deserialize)

    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Integer(-sys.maxsize - 1), "-9223372036854775808"),
            (Integer(3), "3"),
            (Integer(sys.maxsize), "9223372036854775807"),
        ],
    )
    async def test_should_deserialize_integer(self, data_type: Integer, value: str):
        # Create xml
        xml = f"<MaximalInclusive>{value}</MaximalInclusive>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, MaximalInclusive.deserialize, {"data_type": Integer})

        # Assert that the method returns the correct value
        assert constraint == MaximalInclusive(data_type)

    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Real(sys.float_info.min), "2.2250738585072014e-308"),
            (Real(-math.pi), "-3.141592653589793"),
            (Real(3.3), "3.3"),
            (Real(math.pi), "3.141592653589793"),
            (Real(sys.float_info.max), "1.7976931348623157e+308"),
        ],
    )
    async def test_should_deserialize_real(self, data_type: Real, value: str):
        # Create xml
        xml = f"<MaximalInclusive>{value}</MaximalInclusive>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, MaximalInclusive.deserialize, {"data_type": Real})

        # Assert that the method returns the correct value
        assert constraint == MaximalInclusive(data_type)

    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Date(1, 1, 1, timezone=Timezone(hours=-14)), "0001-01-01-14:00"),
            (Date(1, 1, 1), "0001-01-01Z"),
            (Date(1, 1, 1, timezone=Timezone(hours=14)), "0001-01-01+14:00"),
            (Date(2022, 8, 5, timezone=Timezone(hours=-3, minutes=30)), "2022-08-05-02:30"),
            (Date(2022, 8, 5), "2022-08-05-00:00"),
            (Date(2022, 8, 5), "2022-08-05Z"),
            (Date(2022, 8, 5), "2022-08-05+00:00"),
            (Date(2022, 8, 5, timezone=Timezone(hours=2, minutes=30)), "2022-08-05+02:30"),
            (Date(9999, 12, 31, timezone=Timezone(hours=-14)), "9999-12-31-14:00"),
            (Date(9999, 12, 31), "9999-12-31Z"),
            (Date(9999, 12, 31, timezone=Timezone(hours=14)), "9999-12-31+14:00"),
        ],
    )
    async def test_should_deserialize_date(self, data_type: Date, value: str):
        # Create xml
        xml = f"<MaximalInclusive>{value}</MaximalInclusive>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, MaximalInclusive.deserialize, {"data_type": Date})

        # Assert that the method returns the correct value
        assert constraint == MaximalInclusive(data_type)

    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Time(0, 0, 0, 0, timezone=Timezone(hours=-14)), "00:00:00.000-14:00"),
            (Time(0, 0, 0, 0), "00:00:00.000Z"),
            (Time(0, 0, 0, 0, timezone=Timezone(hours=14)), "00:00:00.000+14:00"),
            (Time(12, 34, 56, 789, timezone=Timezone(hours=-3, minutes=30)), "12:34:56.789-02:30"),
            (Time(12, 34, 56, 789), "12:34:56.789-00:00"),
            (Time(12, 34, 56, 789), "12:34:56.789Z"),
            (Time(12, 34, 56, 789), "12:34:56.789+00:00"),
            (Time(12, 34, 56, 789, timezone=Timezone(hours=2, minutes=30)), "12:34:56.789+02:30"),
            (Time(23, 59, 59, 999, timezone=Timezone(hours=-14)), "23:59:59.999-14:00"),
            (Time(23, 59, 59, 999), "23:59:59.999Z"),
            (Time(23, 59, 59, 999, timezone=Timezone(hours=14)), "23:59:59.999+14:00"),
        ],
    )
    async def test_should_deserialize_time(self, data_type: Time, value: str):
        # Create xml
        xml = f"<MaximalInclusive>{value}</MaximalInclusive>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, MaximalInclusive.deserialize, {"data_type": Time})

        # Assert that the method returns the correct value
        assert constraint == MaximalInclusive(data_type)

    @pytest.mark.parametrize(
        ("data_type", "value"),
        [
            (Timestamp(2022, 8, 5, 0, 0, 0, 0, timezone=Timezone(hours=-14)), "2022-08-05T00:00:00.000-14:00"),
            (Timestamp(2022, 8, 5, 0, 0, 0, 0), "2022-08-05T00:00:00.000Z"),
            (Timestamp(2022, 8, 5, 0, 0, 0, 0, timezone=Timezone(hours=14)), "2022-08-05T00:00:00.000+14:00"),
            (
                Timestamp(2022, 8, 5, 12, 34, 56, 789, timezone=Timezone(hours=-3, minutes=30)),
                "2022-08-05T12:34:56.789-02:30",
            ),
            (Timestamp(2022, 8, 5, 12, 34, 56, 789), "2022-08-05T12:34:56.789-00:00"),
            (Timestamp(2022, 8, 5, 12, 34, 56, 789), "2022-08-05T12:34:56.789Z"),
            (Timestamp(2022, 8, 5, 12, 34, 56, 789), "2022-08-05T12:34:56.789+00:00"),
            (
                Timestamp(2022, 8, 5, 12, 34, 56, 789, timezone=Timezone(hours=2, minutes=30)),
                "2022-08-05T12:34:56.789+02:30",
            ),
            (Timestamp(2022, 8, 5, 23, 59, 59, 999, timezone=Timezone(hours=-14)), "2022-08-05T23:59:59.999-14:00"),
            (Timestamp(2022, 8, 5, 23, 59, 59, 999), "2022-08-05T23:59:59.999Z"),
            (Timestamp(2022, 8, 5, 23, 59, 59, 999, timezone=Timezone(hours=14)), "2022-08-05T23:59:59.999+14:00"),
        ],
    )
    async def test_should_deserialize_timestamp(self, data_type: Timestamp, value: str):
        # Create xml
        xml = f"<MaximalInclusive>{value}</MaximalInclusive>"

        # Deserialize
        constraint = Deserializer.deserialize(xml, MaximalInclusive.deserialize, {"data_type": Timestamp})

        # Assert that the method returns the correct value
        assert constraint == MaximalInclusive(data_type)

    async def test_should_raise_on_invalid_data_type(self):
        # Create xml
        xml = "<MaximalInclusive>2</MaximalInclusive>"

        # Deserialize
        with pytest.raises(
            ParseError,
            match=re.escape(
                "Expected constraint's data type to be 'Integer', 'Real', 'Date', 'Time' or 'Timestamp', "
                "received 'String'."
            ),
        ):
            Deserializer.deserialize(xml, MaximalInclusive.deserialize, {"data_type": String})

    async def test_should_raise_on_invalid_value(self):
        # Create xml
        xml = "<MaximalInclusive>X</MaximalInclusive>"

        # Deserialize
        with pytest.raises(
            ParseError, match=re.escape("Could not convert 'MaximalInclusive' with value 'X' to Integer.")
        ):
            Deserializer.deserialize(xml, MaximalInclusive.deserialize, {"data_type": Integer})
