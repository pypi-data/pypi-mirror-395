import datetime
from good_common.utilities._iterators import iter_ranges


def test_date_ranges_with_int_step():
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 1, 5)
    result = list(iter_ranges(start, end, 2))
    expected = [
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 3)),
        (datetime.date(2023, 1, 3), datetime.date(2023, 1, 5)),
    ]
    assert result == expected


def test_datetime_ranges_with_int_step():
    start = datetime.datetime(2023, 1, 1, 12, 0)
    end = datetime.datetime(2023, 1, 3, 12, 0)
    result = list(iter_ranges(start, end, 1))
    expected = [
        (datetime.datetime(2023, 1, 1, 12, 0), datetime.datetime(2023, 1, 2, 12, 0)),
        (datetime.datetime(2023, 1, 2, 12, 0), datetime.datetime(2023, 1, 3, 12, 0)),
    ]
    assert result == expected


def test_date_ranges_with_timedelta_step():
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 1, 5)
    step = datetime.timedelta(days=2)
    result = list(iter_ranges(start, end, step))
    expected = [
        (datetime.date(2023, 1, 1), datetime.date(2023, 1, 3)),
        (datetime.date(2023, 1, 3), datetime.date(2023, 1, 5)),
    ]
    assert result == expected


def test_single_day_range():
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 1, 2)
    result = list(iter_ranges(start, end))
    expected = [(datetime.date(2023, 1, 1), datetime.date(2023, 1, 2))]
    assert result == expected


def test_empty_range():
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 1, 1)
    result = list(iter_ranges(start, end))
    assert result == []


def test_reversed_range():
    start = datetime.date(2023, 1, 5)
    end = datetime.date(2023, 1, 1)
    result = list(iter_ranges(start, end))
    assert result == []


def test_large_step():
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 1, 5)
    result = list(iter_ranges(start, end, 10))
    expected = [(datetime.date(2023, 1, 1), datetime.date(2023, 1, 5))]
    assert result == expected


def test_datetime_with_timedelta():
    start = datetime.datetime(2023, 1, 1, 12, 0)
    end = datetime.datetime(2023, 1, 3, 12, 0)
    step = datetime.timedelta(hours=24)
    result = list(iter_ranges(start, end, step))
    expected = [
        (datetime.datetime(2023, 1, 1, 12, 0), datetime.datetime(2023, 1, 2, 12, 0)),
        (datetime.datetime(2023, 1, 2, 12, 0), datetime.datetime(2023, 1, 3, 12, 0)),
    ]
    assert result == expected


def test_date_ranges_with_negative_int_step():
    start = datetime.date(2023, 1, 5)
    end = datetime.date(2023, 1, 1)
    result = list(iter_ranges(start, end, -2))
    expected = [
        (datetime.date(2023, 1, 5), datetime.date(2023, 1, 3)),
        (datetime.date(2023, 1, 3), datetime.date(2023, 1, 1)),
    ]
    assert result == expected


def test_datetime_ranges_with_negative_timedelta():
    start = datetime.datetime(2023, 1, 3, 12, 0)
    end = datetime.datetime(2023, 1, 1, 12, 0)
    step = datetime.timedelta(hours=-24)
    result = list(iter_ranges(start, end, step))
    expected = [
        (datetime.datetime(2023, 1, 3, 12, 0), datetime.datetime(2023, 1, 2, 12, 0)),
        (datetime.datetime(2023, 1, 2, 12, 0), datetime.datetime(2023, 1, 1, 12, 0)),
    ]
    assert result == expected
