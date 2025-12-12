"""Collection of widget exports"""


from jbqt.widgets.chip_button import ChipButton
from jbqt.widgets.chips import ChipsWidget
from jbqt.widgets.multiselect import MultiSelectComboBox
from jbqt.widgets.simple import ClickableLabel, LongIntSpinBox
from jbqt.widgets.toast import Toast

WIDGET_LIST = [ChipButton, ChipsWidget, MultiSelectComboBox, ClickableLabel, LongIntSpinBox, Toast]


__all__ = [
    "ChipButton",
    "ChipsWidget",
    "MultiSelectComboBox",
    "ClickableLabel",
    "LongIntSpinBox",
    "Toast",
]
