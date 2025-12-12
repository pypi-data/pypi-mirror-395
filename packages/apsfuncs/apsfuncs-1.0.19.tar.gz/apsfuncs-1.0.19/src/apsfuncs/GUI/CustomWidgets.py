from PyQt6.QtWidgets import QGridLayout, QSpacerItem, QWidget, QSizePolicy
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QPainter

from apsfuncs.GUI.BaseWidgets import IconButton

# Create a toolbar widget to contain accessed buttong
class QuickBar(QWidget):
    # Init
    def __init__(self, parent_widget, target_height=None, scaling=1):
        super().__init__()
        self.parent_widget = parent_widget
        self.scaling = scaling
        self.target_height = target_height

        # Add button for settings
        self.settings_button = IconButton(icon="settings.ico")
        self.settings_button.clicked.connect(self.settings_button_clicked)
        self.settings_button.setToolTip("Settings")
        self.settings_button.setMaximumSize(100, 100)

        # Add button for giving feedback
        self.feedback_button = IconButton(icon="feedback.ico")
        self.feedback_button.clicked.connect(self.feedback_button_clicked)
        self.feedback_button.setToolTip("Submit feedback")
        self.feedback_button.setMaximumSize(100, 100)

        # Create the layout for the bar
        layout = QGridLayout()
        self.setLayout(layout)

        # Add the contents to the bar
        layout.addWidget(self.settings_button, 0, 0, 1, 1)
        layout.addWidget(self.feedback_button, 0, 1, 1, 1)
        layout.addItem(QSpacerItem(1, 1, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum), 0, 2, 1, 1)
        
        QTimer.singleShot(0, self.adjust_sizes)

    # define function to return to the main scene
    def settings_button_clicked(self):
        self.parent_widget.main_window.show_target_screen(target="Settings")

    # define function to return to the main scene
    def feedback_button_clicked(self):
        self.parent_widget.main_window.show_target_screen(target="Feedback")

    def adjust_sizes(self):
        # Check if a target height was given, if so then use it
        if self.target_height is not None:
            self.settings_button.setFixedHeight(self.target_height)
            
        # Set the width of the button to the height inclusing the origional scaling
        self.settings_button.setFixedWidth(int(self.settings_button.size().height()*self.scaling))
        self.settings_button.setIconSize(self.settings_button.size())

# Basic widget to display a coloured circle
class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set the colour
        self.colour = QColor(Qt.GlobalColor.gray)
        self.setAutoFillBackground(True)

        self.setStyleSheet("""
                                background-color: rgba(1, 1, 1, 0)
                           """)

    # Override paint event
    def paintEvent(self, a0):

        # Paint the circle
        painter = QPainter(self)
        painter.setBrush(self.colour)
        painter.setPen(Qt.PenStyle.NoPen)

        radius = min(self.width(), self.height())//2

        painter.drawEllipse((self.width() - 2*radius) // 2,
                            (self.height() - 2*radius) //2,
                            2*radius, 2*radius)

        return super().paintEvent(a0)
    
    # Method to update the colour
    def update_colour(self, new_colour):
        self.colour = new_colour
        self.repaint()