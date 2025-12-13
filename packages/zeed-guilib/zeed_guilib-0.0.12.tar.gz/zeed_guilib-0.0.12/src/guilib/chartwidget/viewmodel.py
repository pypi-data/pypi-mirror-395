from datetime import date
from decimal import Decimal
from decimal import InvalidOperation
from functools import partial
from typing import TYPE_CHECKING
from typing import Literal
from typing import cast
from typing import overload
from typing import override

from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QObject
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush
from PySide6.QtGui import QColor

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Sequence

    from PySide6.QtWidgets import QStatusBar

    from guilib.chartwidget.model import InfoProto


def try_else[T](
    fun: 'Callable[[], T]',
    fallback: T,
    *,
    exception_class: type[Exception] = Exception,
) -> T:
    try:
        return fun()
    except exception_class:
        return fallback


def max_min_this(
    data: list[list[str | None]], row: int, column: int
) -> 'tuple[Decimal, Decimal, Decimal|None]':
    ds = (
        [
            None
            if datum[0] is None
            else Decimal(date.fromisoformat(datum[0]).toordinal())
            for datum in data
        ]
        if column == 0
        else [
            None
            if datum[column] is None
            else try_else(
                partial(Decimal, cast('str', datum[column])),
                Decimal(),
                exception_class=InvalidOperation,
            )
            for datum in data
        ]
    )
    return (
        max(d for d in ds if d is not None),
        min(d for d in ds if d is not None),
        ds[row],
    )


_QMODELINDEX = QModelIndex()


def parse_infos(
    infos: 'Sequence[InfoProto]',
) -> tuple[list[str], list[list[str | None]]]:
    headers: list[str] = ['when']
    data: list[list[str | None]] = []

    indexes: dict[str, int] = {}

    for info in infos:
        row: list[str | None] = [None] * len(headers)

        # when
        row[0] = str(info.when)

        # columns
        for columns in sorted(
            info.columns, key=lambda column: column.header.name
        ):
            key = columns.header.name
            value = str(columns.howmuch)
            if key in indexes:
                row[indexes[key]] = value
            else:
                indexes[key] = len(headers)
                headers.append(key)
                for other_row in data:
                    other_row.append(None)
                row.append(value)

        data.append(row)

    return headers, data


class ViewModel(QAbstractTableModel):
    def __init__(self, parent: QObject, infos: 'list[InfoProto]') -> None:
        super().__init__(parent)
        self._set_infos(infos)

    def _set_infos(self, infos: 'Sequence[InfoProto]') -> None:
        self._headers, self._data = parse_infos(infos)
        self._infos = infos

    @override
    def rowCount(
        self, _parent: QModelIndex | QPersistentModelIndex = _QMODELINDEX
    ) -> int:
        return len(self._data)

    @override
    def columnCount(
        self, _parent: QModelIndex | QPersistentModelIndex = _QMODELINDEX
    ) -> int:
        return len(self._headers)

    @override
    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation != Qt.Orientation.Horizontal:
            return None

        return self._headers[section]

    @overload
    def data(
        self,
        # white liar, we need also to add a rule on index --> col 0
        index: QModelIndex | QPersistentModelIndex,
        role: Literal[Qt.ItemDataRole.UserRole],
    ) -> date: ...

    @overload
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | Qt.AlignmentFlag | None | date | Decimal | QBrush: ...

    @override
    def data(  # noqa: PLR0911
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | Qt.AlignmentFlag | None | date | Decimal | QBrush:
        if role in {
            Qt.ItemDataRole.DecorationRole,
            Qt.ItemDataRole.StatusTipRole,
            Qt.ItemDataRole.FontRole,
            Qt.ItemDataRole.ForegroundRole,
            Qt.ItemDataRole.CheckStateRole,
            Qt.ItemDataRole.SizeHintRole,
        }:
            return None

        column = index.column()
        row = index.row()

        if role in {Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole}:
            value = self._data[row][column]
            if value is None:
                return None
            if column == 0:
                return value[:-3] if value.endswith('01') else f'{value[:-5]}13'
            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.BackgroundRole:
            max_, min_, val = max_min_this(self._data, row, column)
            if val is None:
                return None

            perc = (
                (val - min_) / (max_ - min_) if max_ != min_ else Decimal('.5')
            )

            hue = int(perc * 120)  # 0..359 ; red=0, green=120
            saturation = 223  # 0..255
            lightness = 159  # 0..255

            return QBrush(QColor.fromHsl(hue, saturation, lightness))

        if role == Qt.ItemDataRole.UserRole:
            if column == 0:
                return self._infos[row].when

            value = self._data[row][column]
            return Decimal(value) if value is not None else None

        # DisplayRole 0
        # DecorationRole 1
        # EditRole 2
        # ToolTipRole 3
        # StatusTipRole 4
        # WhatsThisRole 5
        # FontRole 6
        # TextAlignmentRole 7
        # BackgroundRole 8
        # ForegroundRole 9
        # CheckStateRole 10
        # AccessibleTextRole 11
        # AccessibleDescriptionRole 12
        # SizeHintRole 13
        # InitialSortOrderRole 14
        # DisplayPropertyRole 27
        # DecorationPropertyRole 28
        # ToolTipPropertyRole 29
        # StatusTipPropertyRole 30
        # WhatsThisPropertyRole 31
        # UserRole 256
        return None

    @override
    def sort(
        self, index: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder
    ) -> None:
        def key(row: list[str | None]) -> date | Decimal | str:
            raw = row[index]
            if raw is None:
                return ''
            if index == 0:
                return date.fromisoformat(raw)
            return Decimal(raw)

        self.layoutAboutToBeChanged.emit()
        try:
            self._data.sort(
                key=key, reverse=order == Qt.SortOrder.AscendingOrder
            )
        finally:
            self.layoutChanged.emit()

    def load(self, infos: 'Sequence[InfoProto]') -> None:
        self.beginResetModel()
        try:
            self._set_infos(infos)
        finally:
            self.endResetModel()


class SortFilterViewModel(QSortFilterProxyModel):
    def __init__(self) -> None:
        super().__init__()
        self.setSourceModel(ViewModel(self, []))
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setDynamicSortFilter(True)

    @override
    def filterAcceptsRow(
        self,
        source_row: int,
        source_parent: QModelIndex | QPersistentModelIndex,
    ) -> bool:
        regex = self.filterRegularExpression()
        source_model = self.sourceModel()
        column_count = source_model.columnCount(source_parent)

        return any(
            regex.match(str(source_model.data(index))).hasMatch()
            for index in (
                source_model.index(source_row, i, source_parent)
                for i in range(column_count)
            )
        )

    def filter_changed(self, text: str) -> None:
        text = QRegularExpression.escape(text)
        options = QRegularExpression.PatternOption.CaseInsensitiveOption
        self.setFilterRegularExpression(QRegularExpression(text, options))

    def sort(
        self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder
    ) -> None:
        self.sourceModel().sort(column, order)

    def selection_changed(
        self, selection_model: QItemSelectionModel, statusbar: 'QStatusBar'
    ) -> None:
        column = selection_model.currentIndex().column()
        if column == 0:
            message = ''
        else:
            bigsum = sum(
                index.data(Qt.ItemDataRole.UserRole)
                for index in selection_model.selectedRows(column)
            )
            message = f'⅀ = {bigsum}'
        statusbar.showMessage(message)

    def update(self, infos: 'Sequence[InfoProto]') -> None:
        self.sourceModel().load(infos)

    def get_categories(self) -> list[str]:
        view_model = self.sourceModel()
        return view_model._headers  # noqa: SLF001

    def get_rows(self) -> 'Sequence[InfoProto]':
        view_model = self.sourceModel()
        return view_model._infos  # noqa: SLF001

    @override
    def sourceModel(self) -> ViewModel:
        return cast('ViewModel', super().sourceModel())
