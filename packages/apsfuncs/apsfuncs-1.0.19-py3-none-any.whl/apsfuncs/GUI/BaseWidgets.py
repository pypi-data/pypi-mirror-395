import os

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QPushButton, QScrollArea, QProgressBar, QToolBox, QLineEdit, QDoubleSpinBox, QSpinBox, QCheckBox
from PyQt6.QtWidgets import QLineEdit, QPlainTextEdit, QSlider, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QSizePolicy, QVBoxLayout, QHeaderView, QStyle
from PyQt6.QtCore import Qt, QTimer
from PyQt6 import QtGui

from apsfuncs.Toolbox.ConfigHandlers import get_resource_path

"""This file contains a set of base widgets that are slight customisations on default PyQt6 widgets
anything more complex or custom should be put in the CustomWidgets file"""

# A basic label with a given start text
class Label(QLabel):

    def __init__(self, start_text=""):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setText(start_text)

# Set up MplCanvas to plt matplotlib graophs
class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.margins(0, 0.02)
        super().__init__(self.fig)

# Progress bar
class ProgBar(QProgressBar):
    def __init__(self, min=0, max=100):
        super().__init__()
        self.maximum = max
        self.minimum = min

# Toolbox
class ToolBox(QToolBox):
    def __init__(self):
        super().__init__()

# Basic multiline text box
class TextBox(QPlainTextEdit):

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

    # Method to add a new line of text to the box
    def add_line(self, new_line):
        self.appendPlainText(new_line)
# Table
class Table(QTableWidget):
    def __init__(self, rows, columns, width_weights):
        super().__init__()
        self.setRowCount(rows)
        self.setColumnCount(columns)
        self.width_weights = width_weights
        self.total_weight = sum(width_weights)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # Method to resize the column with the set weights
    def update_column_widths(self):
        total_width = self.viewport().width()
        for i, w in enumerate(self.width_weights):
            width = int(total_width * (w / self.total_weight))
            self.setColumnWidth(i, width)

    # Method to override on rezie to reset column widths
    def resizeEvent(self, event):
        self.update_column_widths()
        super().resizeEvent(event)

# Custom read only table item
class DisplayTableItem(QTableWidgetItem):
    def __init__(self, start_text=""):
        super().__init__(start_text)

# Frame widget to act as a divider
class Divider(QFrame):
    def __init__(self, direction):
        super().__init__()
        if direction == "v":
            self.setFrameShape(QFrame.Shape.VLine)
        else:
            self.setFrameShape(QFrame.Shape.HLine)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

# Custom scroll area to only scroll vertically
class CustomVScrollWidget(QScrollArea):
    # init
    def __init__(self):
        super().__init__(widgetResizable=True)
        self.widget_layout = QVBoxLayout()

        # Create the content widget with the given layout and set the size policy
        self.content_widget = QWidget()
        self.content_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.content_widget.setLayout(self.widget_layout)

        # Set the sctroll aread widget and scroll properties
        self.setWidget(self.content_widget)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    # Method to add a widget to the scroll area widget (bypass layout to allow the resize action)
    def add_widget(self, new_widget, dont_resize=False):
        self.widget_layout.addWidget(new_widget)
        if not dont_resize:
            QTimer.singleShot(0, self.adjust_width)

    # Method to adjust the area width
    def adjust_width(self):
        self.setMinimumWidth(self.content_widget.sizeHint().width() + self.verticalScrollBar().width())

    # Method to clear the scroll area
    def clear_widgets(self):
        while self.widget_layout.count():
            child = self.widget_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

# Check box
class CheckBox(QCheckBox):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

# Line text field
class LineTextField(QLineEdit):
    def __init__(self, place_holder_text="", max_length=20):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.setPlaceholderText(place_holder_text)
        self.setMaxLength(max_length)

# Double spin box
class DoubleNumBox(QDoubleSpinBox):
    def __init__(self, max=10, min=1, preffix="", suffix="", step=1):
        super().__init__()
        self.setRange(min, max)
        self.setPrefix(preffix)
        self.setSuffix(suffix)
        self.setSingleStep(step)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

# Int spin box
class NumBox(QSpinBox):
    def __init__(self, max=10, min=1, preffix="", suffix="", step=1):
        super().__init__()
        self.setRange(min, max)
        self.setPrefix(preffix)
        self.setSuffix(suffix)
        self.setSingleStep(step)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

# Date Edit Box
class DateEditBox(QDateEdit):
    def __init__(self, max_date=None, min_date=None, disp_format="dd MMM yyyy"):
        super().__init__()
        if min_date != None:
            self.setMinimumDate(min_date)
        if max_date != None:
            self.setMaximumDate(max_date)
        self.setDisplayFormat(disp_format)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

# Dropdown box
class DropDown(QComboBox):

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

# Slider bar
class Slider(QSlider):
    # init
    def __init__(self, min, max, start_val=None, step=1, direction="Horizontal", tick_interval=1):
        super().__init__()
        if direction == "Horizontal":
            self.setOrientation(Qt.Orientation.Horizontal)
        else:
            self.setOrientation(Qt.Orientation.Vertical)
        self.setRange(min, max)
        self.setSingleStep(step)
        self.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.setTickInterval(tick_interval)
        if start_val is not None:
            self.setValue(start_val)

# Push button
class PushButton(QPushButton):

    def __init__(self, button_text="Default"):
        super().__init__()
        self.setText(button_text)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

# Push button with icon
class IconButton(QPushButton):

    def __init__(self, icon=None, std_icon=None):
        super().__init__()
        # Create the button and set the icon and size (if an icon string is passed or if a standard icon is used)
        if icon is not None:
            self.setIcon(QtGui.QIcon(os.path.join(get_resource_path(), 'icons', icon)))
        else:
            self.setIcon(self.style().standardIcon(getattr(QStyle.StandardPixmap, std_icon)))
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        # Set the stylesheet to hide the background, but also indicate the button when hovering over it, also remove the borders to allo the icon to be full size
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0px;
                margin: 0px;
                background: transparent;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 30);  /* optional hover effect */
            }
        """)
        
    def resizeEvent(self, event):
        # Force the button to be square and fill it with the Icon
        self.setFixedSize(event.size().height(), event.size().height())
        self.setIconSize(self.size())
        super().resizeEvent(event)

# Custom toolbar to hook onto control events
class CustomNavigationToolbar(NavigationToolbar):
    def __init__(self, canvas, parent=None, callback_hook=None):
        super().__init__(canvas, parent)
        self.callback_hook = callback_hook

    def back(self, *args, **kwargs):
        super().back(*args, **kwargs)
        if self.callback_hook:
            self.callback_hook("back")

    def forward(self, *args, **kwargs):
        super().forward(*args, **kwargs)
        if self.callback_hook:
            self.callback_hook("forward")

    def pan(self, *args, **kwargs):
        super().pan(*args, **kwargs)
        if self.callback_hook:
            self.callback_hook("pan")

    def zoom(self, *args, **kwargs):
        super().zoom(*args, **kwargs)
        if self.callback_hook:
            self.callback_hook("zoom")
