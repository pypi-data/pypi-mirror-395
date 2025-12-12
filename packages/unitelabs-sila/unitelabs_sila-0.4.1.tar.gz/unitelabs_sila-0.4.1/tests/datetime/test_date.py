import pickle

from sila import datetime


def test_date_should_store_timezone():
    expected = datetime.timezone(offset=datetime.timedelta(hours=+2))
    value = datetime.date(year=2022, month=8, day=5, tzinfo=expected)

    assert value.tzinfo == expected


def test_date_should_pickle():
    expected = datetime.date(year=2022, month=8, day=5, tzinfo=datetime.timezone(offset=datetime.timedelta(hours=+2)))
    value = pickle.dumps(expected)

    assert pickle.loads(value) == expected
