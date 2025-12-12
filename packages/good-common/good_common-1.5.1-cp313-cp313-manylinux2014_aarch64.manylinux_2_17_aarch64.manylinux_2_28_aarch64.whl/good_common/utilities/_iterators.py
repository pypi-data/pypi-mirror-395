import datetime
from typing import Union, Tuple, Generator, overload

DateType = Union[datetime.date, datetime.datetime]
StepType = Union[int, datetime.timedelta]


@overload
def iter_ranges(
    start: datetime.datetime, end: datetime.datetime, step: int = 1
) -> Generator[Tuple[datetime.datetime, datetime.datetime], None, None]: ...


@overload
def iter_ranges(
    start: datetime.datetime, end: datetime.datetime, step: datetime.timedelta
) -> Generator[Tuple[datetime.datetime, datetime.datetime], None, None]: ...


@overload
def iter_ranges(
    start: datetime.date, end: datetime.date, step: int = 1
) -> Generator[Tuple[datetime.date, datetime.date], None, None]: ...


@overload
def iter_ranges(
    start: datetime.date, end: datetime.date, step: datetime.timedelta
) -> Generator[Tuple[datetime.date, datetime.date], None, None]: ...


def iter_ranges(
    start: DateType, end: DateType, step: StepType = 1
) -> Generator[Tuple[DateType, DateType], None, None]:
    if isinstance(step, int):
        if step == 0:
            raise ValueError("step cannot be zero")
        delta = datetime.timedelta(days=step)
    else:
        if step == datetime.timedelta(0):
            raise ValueError("step cannot be zero")
        delta = step

    current = start
    if delta > datetime.timedelta(0):
        while current < end:
            next_date = min(current + delta, end)
            yield current, next_date
            current = next_date
    else:
        while current > end:
            next_date = max(current + delta, end)
            yield current, next_date
            current = next_date
