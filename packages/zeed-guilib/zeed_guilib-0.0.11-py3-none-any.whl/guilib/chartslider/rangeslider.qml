import QtQuick
import QtQuick.Controls

RangeSlider {
    orientation: Qt.Horizontal

    signal first_moved(real first_value)
    signal second_moved(real second_value)

    function set_first_value(first_value) {
        first.value = first_value
    }

    function set_second_value(second_value) {
        second.value = second_value
    }

    first.onMoved: first_moved(first.value)
    second.onMoved: second_moved(second.value)
}
