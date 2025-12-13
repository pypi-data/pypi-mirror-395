from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from typing import Final
from typing import cast
from typing import override

from PySide6.QtCharts import QChartView
from PySide6.QtCharts import QValueAxis
from PySide6.QtCore import QPointF
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot

from guilib.chartwidget.chart import Chart
from guilib.chartwidget.charthover import ChartHover
from guilib.chartwidget.datetimeaxis import DateTimeAxis
from guilib.dates.converters import days2date

if TYPE_CHECKING:
    from PySide6.QtCharts import QLineSeries
    from PySide6.QtGui import QMouseEvent
    from PySide6.QtWidgets import QWidget

    from guilib.chartwidget.modelgui import SeriesModelFactory
    from guilib.chartwidget.viewmodel import SortFilterViewModel


def tick_interval(y_max: float, n: int = 10) -> float:
    """Find the min(10**x) that is > (y_max / n)."""
    goal_step: Final = y_max / n
    exp: int = 1
    while True:
        y_step = 10.0**exp
        if y_step > goal_step:
            return y_step
        exp += 1


class ChartView(QChartView):
    def __init__(
        self,
        model: 'SortFilterViewModel',
        parent: 'QWidget | None',
        factory: 'SeriesModelFactory',
        precision: str,
    ) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        self._model = model.sourceModel()
        self._model.modelReset.connect(self.model_reset)
        self._axis_x: DateTimeAxis | None = None
        self._axis_y: QValueAxis | None = None
        self._start_date: date | None = None
        self._end_date: date | None = None
        self._min_money: Decimal | None = None
        self._max_money: Decimal | None = None
        self.chart_hover = ChartHover(precision)
        self.event_pos: QPointF | None = None
        self.factory = factory

    @Slot(date)
    def start_date_changed(self, start_date: date) -> None:
        self._start_date = start_date
        self._date_changed()

    @Slot(date)
    def end_date_changed(self, end_date: date) -> None:
        self._end_date = end_date
        self._date_changed()

    def _date_changed(self) -> None:
        chart = cast('Chart', self.chart())
        axis_x = self._axis_x
        if chart is None or axis_x is None:
            return

        start_date = (
            self._start_date
            if self._start_date is not None
            else axis_x.min_date
        )
        end_date = (
            self._end_date if self._end_date is not None else axis_x.max_date
        )
        chart.x_zoom(start_date, end_date)

    @Slot(date)
    def min_money_changed(self, min_money: Decimal) -> None:
        self._min_money = min_money
        self._money_changed()

    @Slot(date)
    def max_money_changed(self, max_money: Decimal) -> None:
        self._max_money = max_money
        self._money_changed()

    def _money_changed(self) -> None:
        chart = cast('Chart', self.chart())
        axis_y = self._axis_y
        if chart is None or axis_y is None:
            return

        min_money = (
            self._min_money
            if self._min_money is not None
            else Decimal(axis_y.min())
        )
        max_money = (
            self._max_money
            if self._max_money is not None
            else Decimal(axis_y.max())
        )
        chart.y_zoom(min_money, max_money)

    @Slot()
    def model_reset(self) -> None:
        series_model = self.factory(self._model._infos)  # noqa: SLF001

        self.chart_hover.set_unit(series_model.unit)

        chart = Chart()
        chart.replace_series(series_model.series)

        axis_x = DateTimeAxis(series_model.x_min, series_model.x_max)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        for serie in series_model.series:
            serie.attachAxis(axis_x)

        axis_y = QValueAxis(self)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        for serie in series_model.series:
            serie.attachAxis(axis_y)
        axis_y.setTickType(QValueAxis.TickType.TicksDynamic)
        axis_y.setTickAnchor(0.0)
        axis_y.setMinorTickCount(9)
        axis_y.setTickInterval(tick_interval(series_model.y_max))
        axis_y.setMin(series_model.y_min)
        axis_y.setMax(series_model.y_max)

        self.setChart(chart)
        self.chart_hover.setParentItem(chart)
        self._axis_x = axis_x
        self._axis_y = axis_y

    @override
    def mouseMoveEvent(self, event: 'QMouseEvent') -> None:
        chart = self.chart()
        if chart is not None:
            event_pos = event.position()
            event_value = chart.mapToValue(event_pos)

            # find closest x
            # assumption: all series have same x, so just get the first one
            series = cast('list[QLineSeries]', chart.series())
            points = series[0].points()
            _, index, value = min(
                (abs(event_value.x() - point.x()), i, point)
                for i, point in enumerate(points)
            )
            # search if biggish indexes have same point value
            tmp = index
            prev: int | None = None
            while tmp < len(points) and points[tmp].x() == value.x():
                prev = tmp
                tmp += 1
            if prev is not None:
                index = prev
                value = points[prev]

            for serie in series:
                serie.deselectAllPoints()
                serie.selectPoint(index)

            when = days2date(value.x())

            howmuchs = {
                serie.name(): (
                    serie.color(),
                    Decimal(f'{serie.at(index).y():.2f}'),
                )
                for serie in series
            }

            self.event_pos = chart.mapToPosition(value)

            new_x = self.event_pos.x()
            if new_x + self.chart_hover.size().width() > self.size().width():
                new_x -= self.chart_hover.size().width()
            new_y = 100

            self.chart_hover.set_howmuchs(when, howmuchs, QPointF(new_x, new_y))

        super().mouseMoveEvent(event)
        self.update()
