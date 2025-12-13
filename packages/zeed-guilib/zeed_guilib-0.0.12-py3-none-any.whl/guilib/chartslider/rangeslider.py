from abc import abstractmethod
from logging import getLogger
from pathlib import Path
from typing import cast
from typing import override

from PySide6.QtCore import Qt
from PySide6.QtCore import QUrl
from PySide6.QtCore import Signal
from PySide6.QtQuick import QQuickItem
from PySide6.QtQuick import QQuickView

logger = getLogger(__name__)


class RangeSlider(QQuickItem):
    first_moved: Signal
    second_moved: Signal
    orientation: Qt.Orientation = Qt.Orientation.Horizontal

    @abstractmethod
    def set_first_value(self, first_value: float) -> None: ...

    @abstractmethod
    def set_second_value(self, second_value: float) -> None: ...


class RangeSliderView(QQuickView):
    def __init__(self) -> None:
        super().__init__(
            QUrl.fromLocalFile(Path(__file__).with_name('rangeslider.qml'))
        )
        self.statusChanged.connect(self.dump)
        self.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)

    def dump(self, status: QQuickView.Status) -> None:
        if status is QQuickView.Status.Error:
            for error in self.errors():
                logger.error('error=%s', error)

    @override
    def rootObject(self) -> RangeSlider:
        return cast('RangeSlider', super().rootObject())
