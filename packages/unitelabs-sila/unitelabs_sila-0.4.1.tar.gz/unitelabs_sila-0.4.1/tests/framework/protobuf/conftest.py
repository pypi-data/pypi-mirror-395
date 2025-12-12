import math

import pytest

VARINT_TEST_CASES = [
    pytest.param(0, b"\x00", id="min"),
    pytest.param(300, b"\xac\x02", id="single_byte"),
    pytest.param(270549121, b"\x81\x81\x81\x81\x01", id="multi_byte"),
    pytest.param((1 << 63) - 1, b"\xff\xff\xff\xff\xff\xff\xff\xff\x7f", id="max"),
]

UINT32_TEST_CASES = [
    pytest.param(0, b"\x00", id="uint32_min"),
    pytest.param(3, b"\x03", id="3"),
    pytest.param(150, b"\x96\x01", id="150"),
    pytest.param(270, b"\x8e\x02", id="270"),
    pytest.param(86942, b"\x9e\xa7\x05", id="86942"),
    pytest.param(4294967295, b"\xff\xff\xff\xff\x0f", id="uint32_max"),
]

INT32_TEST_CASES = [
    pytest.param(-2147483648, b"\x80\x80\x80\x80\xf8\xff\xff\xff\xff\x01", id="int32_min"),
    pytest.param(-86942, b"\xe2\xd8\xfa\xff\xff\xff\xff\xff\xff\x01", id="-86942"),
    pytest.param(-270, b"\xf2\xfd\xff\xff\xff\xff\xff\xff\xff\x01", id="-270"),
    pytest.param(-150, b"\xea\xfe\xff\xff\xff\xff\xff\xff\xff\x01", id="-150"),
    pytest.param(-2, b"\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01", id="-2"),
    pytest.param(-1, b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01", id="-1"),
    pytest.param(0, b"\x00", id="0"),
    pytest.param(1, b"\x01", id="1"),
    pytest.param(2, b"\x02", id="2"),
    pytest.param(150, b"\x96\x01", id="150"),
    pytest.param(270, b"\x8e\x02", id="270"),
    pytest.param(86942, b"\x9e\xa7\x05", id="86942"),
    pytest.param(2147483647, b"\xff\xff\xff\xff\x07", id="int32_max"),
]

UINT64_TEST_CASES = [
    *UINT32_TEST_CASES,
    pytest.param(18446744073709551615, b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01", id="uint64_max"),
]

INT64_TEST_CASES = [
    pytest.param(-9223372036854775808, b"\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01", id="int64_min"),
    *INT32_TEST_CASES,
    pytest.param(9223372036854775807, b"\xff\xff\xff\xff\xff\xff\xff\xff\x7f", id="int64_max"),
]

DOUBLE_TEST_CASES = [
    pytest.param(-math.inf, b"\x00\x00\x00\x00\x00\x00\xf0\xff", id="negative_inf"),
    pytest.param(-1.7976931348623157e308, b"\xff\xff\xff\xff\xff\xff\xef\xff", id="double_min"),
    pytest.param(-0.1, b"\x9a\x99\x99\x99\x99\x99\xb9\xbf", id="-0.1"),
    pytest.param(0, b"\x00\x00\x00\x00\x00\x00\x00\x00", id="0"),
    pytest.param(0.1, b"\x9a\x99\x99\x99\x99\x99\xb9\x3f", id="0.1"),
    pytest.param(1.7976931348623157e308, b"\xff\xff\xff\xff\xff\xff\xef\x7f", id="double_max"),
    pytest.param(math.inf, b"\x00\x00\x00\x00\x00\x00\xf0\x7f", id="positive_inf"),
]
