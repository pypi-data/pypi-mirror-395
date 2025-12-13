from typing import TYPE_CHECKING
from typing import Literal
from typing import Protocol
from typing import override

if TYPE_CHECKING:
    from collections.abc import Sequence
    from datetime import date
    from decimal import Decimal

ColumnHeaderUnit = Literal['€', 'days', 'hours']


class ColumnHeaderProto(Protocol):
    name: str
    unit: ColumnHeaderUnit


class ColumnProto(Protocol):
    header: ColumnHeaderProto
    howmuch: 'Decimal | None'


class InfoProto(Protocol):
    when: 'date'
    columns: 'Sequence[ColumnProto]'

    def howmuch(self, column_header: ColumnHeaderProto) -> 'Decimal | None': ...


# default impl


class ColumnHeader:
    def __init__(self, name: str, unit: ColumnHeaderUnit) -> None:
        self.name = name
        self.unit = unit

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ColumnHeader):
            return NotImplemented
        return all([self.name == other.name, self.unit == other.unit])

    @override
    def __hash__(self) -> int:
        return hash(self.name + self.unit)


class Column:
    def __init__(
        self, header: 'ColumnHeaderProto', howmuch: 'Decimal | None'
    ) -> None:
        self.header = header
        self.howmuch = howmuch


class Info:
    def __init__(self, when: 'date', columns: 'Sequence[ColumnProto]') -> None:
        self.when = when
        self.columns = columns

    def howmuch(self, column_header: 'ColumnHeaderProto') -> 'Decimal | None':
        for column in self.columns:
            if column.header == column_header:
                return column.howmuch
        return None
