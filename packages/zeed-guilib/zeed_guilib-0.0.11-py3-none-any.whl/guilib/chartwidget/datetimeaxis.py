from typing import TYPE_CHECKING
from typing import cast

from PySide6.QtCharts import QCategoryAxis

from guilib.dates.converters import date2days
from guilib.dates.generators import CreateDaysStepUnit
from guilib.dates.generators import create_days

if TYPE_CHECKING:
    from datetime import datetime

    from PySide6.QtCore import QDateTime
    from PySide6.QtCore import QObject


class DateTimeAxis(QCategoryAxis):
    def __init__(
        self,
        x_min: 'QDateTime',
        x_max: 'QDateTime',
        parent: 'QObject | None' = None,
    ) -> None:
        super().__init__(parent)
        self.setLabelsPosition(
            QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionOnValue
        )
        self.setTruncateLabels(False)

        x_min_date = cast('datetime', x_min.toPython()).date()
        x_max_date = cast('datetime', x_max.toPython()).date()

        self.setStartValue(date2days(x_min_date))

        self.min_date = x_min_date
        self.max_date = x_max_date

        self.setMin(date2days(self.min_date))
        self.setMax(date2days(self.max_date))

        self.reset_categories(unit=CreateDaysStepUnit.year)

    def reset_categories(
        self, *, unit: CreateDaysStepUnit = CreateDaysStepUnit.month
    ) -> None:
        for label in self.categoriesLabels():
            self.remove(label)

        for step in (1, 3, 4, 6, 12, 24, 36, 48):
            days = list(
                create_days(self.min_date, self.max_date, step=step, unit=unit)
            )
            if len(days) < 200:  # noqa: PLR2004 TODO: find good split
                for day in days:
                    self.append(f'{day:%Y-%m-%d}', date2days(day))
                break
