from typing import TYPE_CHECKING

from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QWidget

from guilib.chartslider.xchartslider import XChartSlider
from guilib.chartslider.ychartslider import YChartSlider
from guilib.chartwidget.chartview import ChartView

if TYPE_CHECKING:
    from guilib.chartwidget.modelgui import SeriesModelFactory
    from guilib.chartwidget.viewmodel import SortFilterViewModel


class ChartWidget(QWidget):
    """Composition of a ChartView and a slider."""

    def __init__(
        self,
        model: 'SortFilterViewModel',
        parent: QWidget | None,
        factory: 'SeriesModelFactory',
        precision: str = '%B %Y',
    ) -> None:
        super().__init__(parent)

        layout = QGridLayout(self)
        chart_view = ChartView(model, self, factory, precision)
        x_chart_slider = XChartSlider(model, self)
        y_chart_slider = YChartSlider(model, self)
        layout.addWidget(chart_view, 0, 0)
        layout.addWidget(x_chart_slider, 1, 0)
        layout.addWidget(y_chart_slider, 0, 1)

        self.setLayout(layout)

        x_chart_slider.start_date_changed.connect(chart_view.start_date_changed)
        x_chart_slider.end_date_changed.connect(chart_view.end_date_changed)

        y_chart_slider.min_money_changed.connect(chart_view.min_money_changed)
        y_chart_slider.max_money_changed.connect(chart_view.max_money_changed)
