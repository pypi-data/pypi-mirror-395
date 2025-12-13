from typing import override

from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QObject
from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtCore import Qt


class SearchableModel(QSortFilterProxyModel):
    def __init__(
        self, model: QAbstractItemModel, parent: QObject | None = None
    ) -> None:
        super().__init__(parent)
        self.setSourceModel(model)
        self.setFilterKeyColumn(-1)
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    @override
    def setFilterWildcard(self, pattern: str) -> None:
        if ':' in pattern:
            key, value = [e.strip() for e in pattern.split(':', 1)]
            model = self.sourceModel()
            for column in range(model.columnCount()):
                header = model.headerData(column, Qt.Orientation.Horizontal)
                if key == str(header):
                    self.setFilterKeyColumn(column)
                    super().setFilterWildcard(value)
                    return

        self.setFilterKeyColumn(-1)
        super().setFilterWildcard(pattern)
