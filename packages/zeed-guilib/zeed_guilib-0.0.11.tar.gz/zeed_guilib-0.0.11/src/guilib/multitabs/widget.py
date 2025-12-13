from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QWidget


class MultiTabs(QTabWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setTabPosition(QTabWidget.TabPosition.West)

    def add_double_box(self, sheet: QWidget, chart: QWidget, label: str) -> int:
        return self.addTab(DoubleBox(sheet, chart), label)

    def remove_double_box(self, idx: int) -> None:
        self.removeTab(idx)


class DoubleBox(QTabWidget):
    def __init__(
        self, sheet: QWidget, chart: QWidget, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setTabPosition(QTabWidget.TabPosition.South)
        self._sheet_idx = self.addTab(sheet, 'sheet')
        self._chart_idx = self.addTab(chart, 'chart')
