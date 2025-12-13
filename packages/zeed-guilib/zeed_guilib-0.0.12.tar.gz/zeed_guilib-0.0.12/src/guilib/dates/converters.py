from datetime import date
from datetime import timedelta
from typing import Final

from PySide6.QtCore import QDateTime

EPOCH: Final = date(1970, 1, 1)


def date2days(d: date, *, epoch: date = EPOCH) -> int:
    return (d - epoch).days


def days2date(days: float, *, epoch: date = EPOCH) -> date:
    return epoch + timedelta(days=days)


def date2QDateTime(d: date, *, epoch: date = EPOCH) -> QDateTime:  # noqa: N802
    return QDateTime.fromSecsSinceEpoch(int((d - epoch).total_seconds()))
