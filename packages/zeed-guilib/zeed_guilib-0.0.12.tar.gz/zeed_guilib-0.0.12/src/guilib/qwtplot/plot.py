from datetime import date
from datetime import timedelta
from itertools import cycle
from math import inf
from typing import TYPE_CHECKING
from typing import cast
from typing import override

from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
from PySide6.QtGui import QBrush
from PySide6.QtGui import QFont
from PySide6.QtGui import QMouseEvent

from guilib.dates.converters import date2days
from guilib.dates.converters import days2date
from guilib.dates.generators import days
from guilib.dates.generators import months
from guilib.dates.generators import years
from guilib.qwtplot.scaledraw import EuroScaleDraw
from guilib.qwtplot.scaledraw import YearMonthScaleDraw
from qwt.legend import QwtLegend
from qwt.plot import QwtPlot
from qwt.plot_curve import QwtPlotCurve
from qwt.plot_grid import QwtPlotGrid
from qwt.plot_marker import QwtPlotMarker
from qwt.scale_div import QwtScaleDiv
from qwt.symbol import QwtSymbol
from qwt.text import QwtText

if TYPE_CHECKING:
    from collections.abc import Iterable
    from decimal import Decimal

    from PySide6.QtWidgets import QWidget

    from guilib.chartwidget.viewmodel import SortFilterViewModel
    from qwt.legend import QwtLegendLabel
    from qwt.scale_draw import QwtScaleDraw


def linecolors() -> 'Iterable[Qt.GlobalColor]':
    excluded: set[Qt.GlobalColor] = {
        Qt.GlobalColor.transparent,
        Qt.GlobalColor.color0,
        Qt.GlobalColor.color1,
        Qt.GlobalColor.black,
        Qt.GlobalColor.white,
        Qt.GlobalColor.lightGray,
        Qt.GlobalColor.gray,
        Qt.GlobalColor.darkGray,
        Qt.GlobalColor.green,
        Qt.GlobalColor.yellow,
        Qt.GlobalColor.cyan,
    }
    return cycle(filter(lambda c: c not in excluded, Qt.GlobalColor))


class Plot(QwtPlot):
    def __init__(
        self,
        model: 'SortFilterViewModel',
        parent: 'QWidget | None',
        *,
        x_bottom_scale_draw: 'QwtScaleDraw | None' = None,
        y_left_scale_draw: 'QwtScaleDraw | None' = None,
        curve_style: int = QwtPlotCurve.Steps,
    ) -> None:
        super().__init__(parent)
        self._model = model
        self._model.modelReset.connect(self.model_reset)
        self.setCanvasBackground(Qt.GlobalColor.white)
        QwtPlotGrid.make(self, enableminor=(False, True))
        self.setAxisScaleDraw(
            QwtPlot.xBottom, x_bottom_scale_draw or YearMonthScaleDraw()
        )
        self.setAxisScaleDraw(
            QwtPlot.yLeft, y_left_scale_draw or EuroScaleDraw()
        )
        # https://github.com/PlotPyStack/PythonQwt/issues/88
        self.canvas().setMouseTracking(True)
        self.setMouseTracking(True)
        self.insertLegend(QwtLegend(), QwtPlot.TopLegend)
        self.curves: dict[str, QwtPlotCurve] = {}
        self.markers: dict[str, QwtPlotMarker] = {}
        self._curve_style = curve_style

    @Slot()
    def model_reset(self) -> None:
        self.curves.clear()

        min_xdata: float | None = None
        max_xdata: float | None = None

        for i, linecolor in zip(
            range(1, self._model.columnCount()), linecolors(), strict=False
        ):
            xdata: list[float] = []
            ydata: list[float] = []

            header = self._model.headerData(i, Qt.Orientation.Horizontal)
            if not header:
                raise ValueError

            for j in range(self._model.rowCount()):
                when: date = self._model.data(
                    self._model.index(j, 0), Qt.ItemDataRole.UserRole
                )

                howmuch = cast(
                    'Decimal | None',
                    self._model.data(
                        self._model.index(j, i), Qt.ItemDataRole.UserRole
                    ),
                )
                if howmuch is None:
                    continue

                xdata.append(date2days(when))
                ydata.append(float(howmuch))

            if xdata:
                tmp = min(xdata)
                if min_xdata is None or tmp < min_xdata:
                    min_xdata = tmp
                tmp = max(xdata)
                if max_xdata is None or tmp > max_xdata:
                    max_xdata = tmp

            name = header
            self.curves[name] = QwtPlotCurve.make(
                xdata=xdata,
                ydata=ydata,
                title=QwtText.make(
                    f'{name} - ...', weight=QFont.Weight.Bold, color=linecolor
                ),
                plot=self,
                style=self._curve_style,
                linecolor=linecolor,
                linewidth=2,
                antialiased=True,
            )
            self.markers[name] = QwtPlotMarker.make(
                symbol=QwtSymbol.make(
                    style=QwtSymbol.Diamond,
                    brush=QBrush(linecolor),
                    size=QSize(9, 9),
                ),
                plot=self,
                align=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                linestyle=QwtPlotMarker.Cross,
                color=Qt.GlobalColor.gray,
                width=1,
                style=Qt.PenStyle.DashLine,
                antialiased=True,
            )

        if min_xdata is None or max_xdata is None:
            raise ValueError

        self._date_changed(min_xdata, max_xdata)

    @Slot(date)
    def start_date_changed(self, start_date: date) -> None:
        lower_bound = date2days(start_date)
        upper_bound = self.axisScaleDiv(QwtPlot.xBottom).interval().maxValue()

        self._date_changed(lower_bound, upper_bound)

    @Slot(date)
    def end_date_changed(self, end_date: date) -> None:
        lower_bound = self.axisScaleDiv(QwtPlot.xBottom).interval().minValue()
        upper_bound = date2days(end_date)

        self._date_changed(lower_bound, upper_bound)

    def _date_changed(self, lower_bound: float, upper_bound: float) -> None:
        ds = days(lower_bound, upper_bound)
        ms = months(lower_bound, upper_bound)
        ys = years(lower_bound, upper_bound)

        # ticks cannot be of len==1
        if len(ds) == 1:
            ds = []
        if len(ms) == 1:
            ms = []
        if len(ys) == 1:
            ys = []

        self.setAxisScaleDiv(
            QwtPlot.xBottom, QwtScaleDiv(lower_bound, upper_bound, ds, ms, ys)
        )

        y_min, y_max = inf, -inf
        for curve in self.curves.values():
            data = curve.data()
            if data is None:
                raise ValueError
            ys = data.yData()
            ys2 = [
                ys[idx]
                for idx, x in enumerate(data.xData())
                if lower_bound <= x <= upper_bound
            ]
            if ys2:
                y_min = min(y_min, *ys2)
                y_max = max(y_max, *ys2)

        self.setAxisScale(QwtPlot.yLeft, y_min, y_max)

        self.replot()

    @Slot(date)
    def min_money_changed(self, min_money: 'Decimal') -> None:
        lower_bound = float(min_money)
        upper_bound = self.axisScaleDiv(QwtPlot.yLeft).interval().maxValue()

        self._money_changed(lower_bound, upper_bound)

    @Slot(date)
    def max_money_changed(self, max_money: 'Decimal') -> None:
        lower_bound = self.axisScaleDiv(QwtPlot.yLeft).interval().minValue()
        upper_bound = float(max_money)

        self._money_changed(lower_bound, upper_bound)

    def _money_changed(self, lower_bound: float, upper_bound: float) -> None:
        self.setAxisScale(QwtPlot.yLeft, lower_bound, upper_bound)

    @override
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        event_pos = event.position()

        scale_map = self.canvasMap(QwtPlot.xBottom)
        event_pos_x = event_pos.x()

        magic_offset = 75  # minimum event_pos_x - TODO: find origin

        dt_hover = days2date(scale_map.invTransform(event_pos_x - magic_offset))

        for name, curve in self.curves.items():
            legend = cast(
                'QwtLegendLabel',
                cast('QwtLegend', self.legend()).legendWidget(curve),
            )

            data = curve.data()
            if data is None:
                raise ValueError

            x_closest = None
            y_closest = None
            td_min = timedelta.max
            for x_data, y_data in zip(data.xData(), data.yData(), strict=True):
                dt_x = days2date(float(x_data))
                td = dt_hover - dt_x if dt_hover > dt_x else dt_x - dt_hover
                if td < td_min:
                    x_closest = x_data
                    y_closest = y_data
                    td_min = td

            text = QwtText.make(
                f'{name} - € {y_closest:_.2f}',
                weight=QFont.Weight.Bold,
                color=curve.pen().color(),
            )
            legend.setText(text)
            if x_closest is not None:
                self.markers[name].setXValue(x_closest)
            if y_closest is not None:
                self.markers[name].setYValue(y_closest)
            self.markers[name].setLabel(text)

        self.replot()
