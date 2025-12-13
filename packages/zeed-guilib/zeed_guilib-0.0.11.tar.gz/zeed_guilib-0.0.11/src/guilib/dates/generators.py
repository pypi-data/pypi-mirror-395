from datetime import date
from datetime import timedelta
from enum import Enum
from enum import auto
from typing import TYPE_CHECKING

from guilib.dates.converters import date2days
from guilib.dates.converters import days2date

if TYPE_CHECKING:
    from collections.abc import Iterable
    from collections.abc import Iterator


def next_first_of_the_month(day: date, *, delta: int = 1) -> date:
    delta_years, m = divmod(day.month - 1 + delta, 12)
    return date(day.year + delta_years, m + 1, 1)


def next_first_of_the_year(day: date, *, delta: int = 1) -> date:
    return date(day.year + delta, 1, 1)


class CreateDaysStepUnit(Enum):
    month = auto()
    year = auto()


def create_days(
    begin: date,
    end: date,
    *,
    step: int = 1,
    unit: CreateDaysStepUnit = CreateDaysStepUnit.month,
) -> 'Iterator[date]':
    """Yield all the first day of the month/year between begin and end."""
    day = begin
    while True:
        yield day
        op = (
            next_first_of_the_month
            if unit is CreateDaysStepUnit.month
            else next_first_of_the_year
        )
        next_day = op(day, delta=step)
        if next_day > end:
            break
        day = next_day


def days(min_xdata: float, max_xdata: float) -> list[float]:
    lower = days2date(min_xdata)
    upper = days2date(max_xdata)

    def it() -> 'Iterable[float]':
        when = lower
        while when <= upper:
            yield date2days(when)
            when += timedelta(days=7)

    return list(it())


def months(min_xdata: float, max_xdata: float) -> list[float]:
    lower = days2date(min_xdata)
    upper = days2date(max_xdata)

    ly, lm = (lower.year, lower.month)
    uy, um = (upper.year, upper.month)

    def it() -> 'Iterable[float]':
        wy, wm = ly, lm
        while (wy, wm) <= (uy, um):
            yield date2days(date(wy, wm, 1))
            if wm < 12:  # noqa: PLR2004
                wm += 1
            else:
                wy += 1
                wm = 1

    return list(it())


def years(min_xdata: float, max_xdata: float) -> list[float]:
    lower = days2date(min_xdata)
    upper = days2date(max_xdata)

    ly = lower.year
    uy = upper.year

    def it() -> 'Iterable[float]':
        wy = ly
        while wy <= uy:
            yield date2days(date(wy, 1, 1))
            wy += 1

    return list(it())
