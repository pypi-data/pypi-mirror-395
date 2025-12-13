from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
from enum import auto
from typing import TYPE_CHECKING

from PySide6.QtCharts import QLineSeries

from guilib.dates.converters import date2days
from guilib.dates.converters import date2QDateTime

if TYPE_CHECKING:
    from collections.abc import Sequence

    from PySide6.QtCore import QDateTime

    from guilib.chartwidget.model import ColumnHeaderProto
    from guilib.chartwidget.model import InfoProto


class SeriesModelUnit(Enum):
    EURO = auto()
    HOUR = auto()
    DAY = auto()


SeriesModelFactory = Callable[['Sequence[InfoProto]'], 'SeriesModel']


@dataclass
class SeriesModel:
    series: 'list[QLineSeries]'
    x_min: 'QDateTime'
    x_max: 'QDateTime'
    y_min: float
    y_max: float
    unit: 'SeriesModelUnit'

    @staticmethod
    def by_column_header(
        *column_headers: 'ColumnHeaderProto',
    ) -> 'SeriesModelFactory':
        def factory(infos: 'Sequence[InfoProto]') -> 'SeriesModel':
            x_min = date.max
            x_max = date.min
            y_min = Decimal('inf')
            y_max = -Decimal('inf')

            line_seriess = []
            for column_header in column_headers:
                line_series = QLineSeries()
                line_series.setName(column_header.name)
                for info in infos:
                    when = info.when
                    howmuch = info.howmuch(column_header)
                    if howmuch is None:
                        continue

                    x_min = min(when, x_min)
                    x_max = max(when, x_max)

                    y_min = min(howmuch, y_min)
                    y_max = max(howmuch, y_max)

                    line_series.append(date2days(when), float(howmuch))
                line_seriess.append(line_series)

            return SeriesModel(
                line_seriess,
                date2QDateTime(x_min),
                date2QDateTime(x_max),
                float(y_min),
                float(y_max),
                SeriesModelUnit.EURO,
            )

        return factory
