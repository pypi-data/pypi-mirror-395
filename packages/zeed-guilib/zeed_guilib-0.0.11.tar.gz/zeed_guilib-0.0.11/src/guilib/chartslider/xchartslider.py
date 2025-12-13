from datetime import date
from logging import getLogger

from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from guilib.chartslider.rangeslider import RangeSliderView
from guilib.dates.converters import date2days
from guilib.dates.converters import days2date

logger = getLogger(__name__)


class XChartSlider(QWidget):
    start_date_changed = Signal(date)
    end_date_changed = Signal(date)

    def __init__(
        self,
        model: QSortFilterProxyModel,
        parent: QWidget | None = None,
        dates_column: int = 0,
    ) -> None:
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.view = RangeSliderView()

        self.range_slider = self.view.rootObject()
        self.range_slider.setProperty('orientation', Qt.Orientation.Horizontal)

        container = QWidget.createWindowContainer(self.view)
        container.setMinimumSize(100, 10)
        layout.addWidget(container)

        self._model = model
        self._model.sourceModel().modelReset.connect(self.source_model_reset)

        def _start_date_changed(days: int) -> None:
            self.start_date_changed.emit(days2date(days))

        self.range_slider.first_moved.connect(_start_date_changed)

        def _end_date_changed(days: int) -> None:
            self.end_date_changed.emit(days2date(days))

        self.range_slider.second_moved.connect(_end_date_changed)
        self.dates_column = dates_column

    @Slot()
    def source_model_reset(self) -> None:
        source_model = self._model.sourceModel()
        dates: list[date] = [
            source_model.data(
                source_model.createIndex(row, self.dates_column),
                Qt.ItemDataRole.UserRole,
            )
            for row in range(source_model.rowCount())
        ]
        if not dates:
            logger.error('no dates!')
            return
        dates.sort()
        minimum = date2days(dates[0])
        maximum = date2days(dates[-1])

        self.range_slider.setProperty('from', minimum)
        self.range_slider.setProperty('to', maximum)
        self.range_slider.set_first_value(minimum)
        self.range_slider.set_second_value(maximum)
