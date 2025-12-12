import os
import shutil
import datetime

from PyQt6.QtWidgets import QFrame, QSizePolicy, QGridLayout, QPlainTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer

from apsfuncs.GUI.BaseWidgets import Label, PushButton
from apsfuncs.Toolbox.ConfigHandlers import get_held_feedback_path
from apsfuncs.Toolbox.GlobalTools import BlackBoard

# Widget for displaying after a crash
class FeedbackScreen(QFrame):

    # Init
    def __init__(self, feedback_name, main_window, current_version):
        super().__init__()
        self.current_version = current_version
        self.main_window = main_window
        self.feedback_name = feedback_name

        # Set up class reference to global black board
        self.bb = BlackBoard.instance()

        # Set up the frame display settings
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)

        # Create a button to submit the feedback file
        submit_button = PushButton(button_text="Submit feedback")
        submit_button.clicked.connect(self.submit_feedback)

        # Create button to cancel without giving feedback
        cancel_button = PushButton(button_text="Cancel")
        cancel_button.clicked.connect(self.cancel_feedback)

        # Create a text field so the user can enter feedback
        self.user_comment_field = QPlainTextEdit()
        self.user_comment_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.user_comment_field.setFont(QFont ( "Arial", 14))

        feedback_label = Label(start_text="Thank you for your feedback, please enter it here and press submit")
        feedback_label.setWordWrap(True)
        feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        feedback_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        feedback_label.setFont(QFont ( "Arial", 20))

        # Add the crash screen components to the screen
        widget_layout = QGridLayout()
        widget_layout.addWidget(feedback_label, 0, 0, 1, 2)
        widget_layout.addWidget(self.user_comment_field, 1, 0, 1, 2)
        widget_layout.addWidget(submit_button, 2, 0, 1, 1)
        widget_layout.addWidget(cancel_button, 2, 1, 1, 1)

        self.setLayout(widget_layout)
        QTimer.singleShot(0, self.adjust_spacing)

    # Method to update the current version once it has been loaded in 
    def update_current_version(self, current_version):
        self.current_version = current_version

    # Method to cancel feeback and return to the previous screen
    def cancel_feedback(self):
        self.bb.logger.info("Canceling feedback")

        # Clear the feedback text
        self.user_comment_field.clear()

        # Return the uer to the previous screen
        self.main_window.show_previous_screen()

    # Method to submit the feeback
    def submit_feedback(self):        
        # Add the user comment to the log file
        self.bb.logger.info("User submitting feedback")

        # Set the feedback filename 
        dt = datetime.datetime.now()
        feedback_filename = self.feedback_name + "Feedback_" + str(dt.year) + "_" + str(dt.month) + "_" + str(dt.day) + "_" + str(dt.hour) + str(dt.minute) + str(dt.second) + ".txt"
        
        # Check if a held feeback folder exists, if not then make is
        if not os.path.exists(get_held_feedback_path()):
            os.mkdir(get_held_feedback_path())

        # Join the feedback file name to the held feedback path
        feedback_filepath = os.path.join(get_held_feedback_path(), feedback_filename)

        # Create a feedback file and add the content to to
        with open(feedback_filepath, "x") as feedback_file:
            feedback_file.write("Logged user: {}\n".format(os.getlogin()))
            feedback_file.write("Software version: {}\n".format(self.current_version))
            feedback_file.write("User comment: \n{}".format(self.user_comment_field.toPlainText()))
            
        # Clear the feedback text
        self.user_comment_field.clear()

        # Try to put the feedback file in the external feedback repo
        remote_dst_file = os.path.join(self.bb.config_dict["Feedback_repo"], feedback_filename)
        try:
            shutil.copyfile(src=feedback_filepath, dst=remote_dst_file)

            # If the file was moved to the external repo then delete it from the held feedback
            os.remove(feedback_filepath)
        except Exception as e:
            # Log the failure and return
            self.bb.logger.info("Failed to save feedback to external repo")
        
        # Close the submit screen to show the previous screen
        self.main_window.show_previous_screen()

    # Method to resize the frame contents
    def adjust_spacing(self):
        # Calcualte the margin spacings and set the contenets margins
        width_spacing = int(self.screen().size().width() * 0.25)
        height_spacing = int(self.screen().size().height() * 0.25)
        self.setContentsMargins(width_spacing, height_spacing, width_spacing, height_spacing)
        
    # Method to call updates on the scene being re-opened
    def scene_opened(self):
        pass