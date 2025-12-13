from decimal import Decimal
from logging import getLogger
from math import inf

from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QWidget

from guilib.chartslider.rangeslider import RangeSliderView

logger = getLogger(__name__)


class YChartSlider(QWidget):
    min_money_changed = Signal(Decimal)
    max_money_changed = Signal(Decimal)

    def __init__(
        self,
        model: QSortFilterProxyModel,
        parent: QWidget | None = None,
        dates_column: int = 0,
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.view = RangeSliderView()

        self.range_slider = self.view.rootObject()
        self.range_slider.setProperty('orientation', Qt.Orientation.Vertical)

        container = QWidget.createWindowContainer(self.view)
        container.setMinimumSize(10, 100)
        layout.addWidget(container)

        self._model = model
        self._model.sourceModel().modelReset.connect(self.source_model_reset)

        def _min_money_changed(money: float) -> None:
            self.min_money_changed.emit(Decimal(money))

        self.range_slider.first_moved.connect(_min_money_changed)

        def _max_money_changed(money: float) -> None:
            self.max_money_changed.emit(Decimal(money))

        self.range_slider.second_moved.connect(_max_money_changed)
        self.dates_column = dates_column

    @Slot()
    def source_model_reset(self) -> None:
        source_model = self._model.sourceModel()
        minimum = inf
        maximum = -inf
        for row in range(source_model.rowCount()):
            for col in range(source_model.columnCount()):
                if col == self.dates_column:
                    continue
                d: Decimal = source_model.data(
                    source_model.createIndex(row, col), Qt.ItemDataRole.UserRole
                )
                value = float(d)
                minimum = min(minimum, value)
                maximum = max(maximum, value)

        self.range_slider.setProperty('from', minimum)
        self.range_slider.setProperty('to', maximum)
        self.range_slider.set_first_value(minimum)
        self.range_slider.set_second_value(maximum)
