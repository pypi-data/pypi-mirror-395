from typing import TYPE_CHECKING
from typing import cast

from PySide6.QtCharts import QAbstractSeries
from PySide6.QtCharts import QChart
from PySide6.QtCharts import QLineSeries
from PySide6.QtCore import Qt

from guilib.dates.converters import date2days

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import date
    from decimal import Decimal

    from guilib.chartwidget.datetimeaxis import DateTimeAxis


class Chart(QChart):
    def __init__(self) -> None:
        super().__init__()
        self.setAcceptHoverEvents(True)
        self.legend().hide()
        self._series: list[QAbstractSeries] = []
        self.scrolledTo = 0.0

    def x_zoom(self, start_date: 'date', end_date: 'date') -> None:
        axis = cast('DateTimeAxis', self.axes(Qt.Orientation.Horizontal)[0])

        axis.setMin(date2days(start_date))
        axis.setMax(date2days(end_date))

    def y_zoom(self, min_money: 'Decimal', max_money: 'Decimal') -> None:
        axis = cast('DateTimeAxis', self.axes(Qt.Orientation.Vertical)[0])

        axis.setMin(float(min_money))
        axis.setMax(float(max_money))

    def replace_series(self, series: 'Iterable[QLineSeries]') -> None:
        self.removeAllSeries()
        self._series.clear()
        for serie in series:
            self.addSeries(serie)
            self._series.append(serie)

    def series(self) -> list[QAbstractSeries]:
        return self._series
