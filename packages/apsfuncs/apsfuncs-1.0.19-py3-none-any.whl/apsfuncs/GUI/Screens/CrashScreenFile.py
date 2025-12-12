import os, sys, shutil

from PyQt6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QPlainTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer

from apsfuncs.GUI.BaseWidgets import Label, PushButton
from apsfuncs.Toolbox.ConfigHandlers import get_crash_log_path, get_logs_path
from apsfuncs.Toolbox.GlobalTools import BlackBoard

# Widget for displaying after a crash
class CrashScreen(QFrame):

    # Init
    def __init__(self, current_log_name):
        super().__init__()
        self.current_log_name = current_log_name

        # Set up class reference to global black board
        self.bb = BlackBoard.instance()

        # Set up the frame display settings
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)

        # Create a button to submit the crash log
        submit_button = PushButton(button_text="Submit crash report and exit")
        submit_button.clicked.connect(self.post_crash_log)

        # Create a text field so the user can submit a crash report comment
        self.user_comment_field = QPlainTextEdit()
        self.user_comment_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.user_comment_field.setFont(QFont ( "Arial", 14))

        error_label = Label(start_text="A fatal error occured, please make a short comment of what you were trying to do when the program crashed")
        error_label.setWordWrap(True)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        error_label.setFont(QFont ( "Arial", 20))

        # Add the crash screen components to the screen
        widget_layout = QVBoxLayout()
        widget_layout.addWidget(error_label)
        widget_layout.addWidget(self.user_comment_field)
        widget_layout.addWidget(submit_button)

        self.setLayout(widget_layout)
        QTimer.singleShot(0, self.adjust_spacing)

    # Method to resize the frame contents
    def adjust_spacing(self):
        # Calcualte the margin spacings and set the contenets margins
        width_spacing = int(self.screen().size().width() * 0.25)
        height_spacing = int(self.screen().size().height() * 0.25)
        self.setContentsMargins(width_spacing, height_spacing, width_spacing, height_spacing)
        
    # Method to call updates on the scene being re-opened
    def scene_opened(self):
        pass

    def post_crash_log(self):  
        # Add the user comment to the log file
        self.bb.logger.info("User comment: {}".format(self.user_comment_field.toPlainText()))

        # Try to put the crash log file in the external crash repo
        src_file = os.path.join(get_logs_path(), self.current_log_name)
        remote_dst_file = os.path.join(self.bb.config_dict["Crash_log_repo"], self.current_log_name)
        try:
            shutil.copyfile(src=src_file, dst=remote_dst_file)
        except Exception as e:
            # Check if there is already a crash logs folder, if not then make on
            if not os.path.exists(get_crash_log_path()):
                os.mkdir(get_crash_log_path())      

            # Put it into the crash log folder
            local_dst_file = os.path.join(get_crash_log_path(), self.current_log_name)
            shutil.copyfile(src=src_file, dst=local_dst_file)
        sys.exit()
        
        