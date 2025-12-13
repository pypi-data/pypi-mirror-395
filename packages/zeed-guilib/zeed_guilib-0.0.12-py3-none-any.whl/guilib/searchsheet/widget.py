from typing import TYPE_CHECKING
from typing import Self

from PySide6.QtCore import QItemSelectionModel
from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtGui import QShortcut
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QAbstractScrollArea
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QWidget

if TYPE_CHECKING:
    from guilib.searchsheet.model import SearchableModel


class SearchSheet(QWidget):
    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
        table_view: QTableView | None = None,
    ) -> None:
        super().__init__(parent, flags)

        self.table_view = QTableView(self) if table_view is None else table_view
        self.table_view.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.table_view.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers  # @UndefinedVariable
        )
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table_view.setShowGrid(True)
        self.table_view.setGridStyle(Qt.PenStyle.DashLine)
        self.table_view.setSortingEnabled(True)
        self.table_view.setWordWrap(False)
        self.table_view.horizontalHeader().setCascadingSectionResizes(True)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().setVisible(False)

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText('Filter')
        self.line_edit.textChanged.connect(self._line_edit_changed)

        layout = QGridLayout(self)
        layout.addWidget(self.table_view, 0, 0, 1, 1)
        layout.addWidget(self.line_edit, 1, 0, 1, 1)
        self.setLayout(layout)

        QShortcut(QKeySequence('Ctrl+F'), self).activated.connect(
            self.line_edit.setFocus
        )
        QShortcut(QKeySequence('Esc'), self).activated.connect(
            lambda: self.line_edit.setText('')
        )

    def _line_edit_changed(self, text: str) -> None:
        model = self.table_view.model()
        if isinstance(model, QSortFilterProxyModel):
            model.setFilterWildcard(text)

    def set_model(self, searchable_model: 'SearchableModel') -> Self:
        self.table_view.setModel(searchable_model)
        searchable_model.modelReset.connect(
            self.table_view.resizeColumnsToContents
        )
        return self

    def selection_model(self) -> QItemSelectionModel:
        return self.table_view.selectionModel()

    def reload(self) -> Self:
        model = self.table_view.model()
        if hasattr(model, 'reload'):
            model.reload()
        return self
