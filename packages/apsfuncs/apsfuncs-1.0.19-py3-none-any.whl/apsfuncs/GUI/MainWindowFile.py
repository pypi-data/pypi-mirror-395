import os

from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QStyle
from PyQt6.QtCore import Qt

from apsfuncs.GUI.Screens.LoadingScreen import LoadingScreen
from apsfuncs.GUI.Screens.CrashScreenFile import CrashScreen
from apsfuncs.GUI.Screens.FeedbackScreenFile import FeedbackScreen

from apsfuncs.GUI.StyleSheets.TitleThemeHandling import TitleThemeManager

from apsfuncs.Toolbox.GlobalTools import BlackBoard

class MainWindowAPSBase(QMainWindow):

    def __init__(self, program_title, feedback_name, main_screen, log_filename, default_screen_name):
        super().__init__()

        self.main_screen = main_screen
        self.current_version = "vX.X.X"
        self.default_screen_name = default_screen_name
        self.program_title = program_title

        # Set up class reference to global black board
        self.bb = BlackBoard.instance()
        
        # Set up flag for page history storage
        self.screen_returning = False

        # Define the stack widget and app data book 
        self.stack = QStackedWidget()
        self.stack.currentChanged.connect(self.update_scene_content)

        # Create dictionary of scene names to index
        self.screen_dict = {}
        self.stack_dict = {}

        # Create a list of the screens that need to listen to live upodates on teh config dict (read for a change, not at runtime values)
        self.config_change_listener_screens = []

        # Add scenes to the stack in thr order matching the stack dictionary
        self.stack.blockSignals(True)

        # Add a crash screen for error handling
        self.crash_screen = CrashScreen(current_log_name=log_filename)
        self.screen_dict["Crash"] = len(self.screen_dict)
        self.stack_dict["Crash"] = self.crash_screen
        self.stack.addWidget(self.crash_screen)

        # Add a crash screen for error handling
        self.feedback_screen = FeedbackScreen(feedback_name=feedback_name, main_window=self, current_version=self.current_version)
        self.screen_dict["Feedback"] = len(self.screen_dict)
        self.stack_dict["Feedback"] = self.feedback_screen
        self.stack.addWidget(self.feedback_screen)

        # Add the main program loading screen
        self.loading_screen = LoadingScreen(main_window=self)
        
        # Stop blocking the stakc signals
        self.stack.blockSignals(False)

    
    # Hook to show event to add the window to the title theme manager
    def showEvent(self, e):
        super().showEvent(e)
        TitleThemeManager.instance().register_window(self)

    # Method to call a config file re-read to all screens that use this
    def call_config_change_listeners(self):
        for screen in self.config_change_listener_screens:
            screen.config_update_event()

    # Method to show the previous screen
    def show_previous_screen(self):
        # Flag that a previous screen is being shown
        self.screen_returning = True

        # Log the screen even and set the screen based on the page history
        self.bb.logger.info("Returning to previous screen")
        self.stack.setCurrentIndex(self.bb.page_history[-2])
        self.bb.page_history.appendleft(self.screen_dict[self.default_screen_name])

    # Method to move to a targt screen
    def show_target_screen(self, target):
        self.stack.setCurrentIndex(self.screen_dict[target])

    # Method to call scene updates 
    def update_scene_content(self, new_index):
        # If a previous screen is not being shown, then append the screen number as the next page in the history, otherwise reset the flag
        if not self.screen_returning:
            self.bb.page_history.append(new_index)
        else:
            self.screen_returning = False

        # Open the target screen
        self.bb.logger.info("Opening {}".format(list(self.screen_dict.keys())[list(self.screen_dict.values()).index(self.stack.currentIndex())]))
        self.stack_dict[list(self.screen_dict.keys())[list(self.screen_dict.values()).index(new_index)]].scene_opened()

    # Method to catch close event (to close down the log)
    def closeEvent(self, event):
         self.bb.logger.info('Log closed')

    # Method if an unhandled exception was caught (crash screen)
    def display_crash_screen(self):
        self.bb.logger.info("Crash detected")
        self.bb.logger.info("Logged user: {}".format(os.getlogin()))
        self.bb.logger.info("Software version: {}".format(self.current_version))
        self.bb.logger.info("Crashed on the {} screen".format(list(self.screen_dict.keys())[list(self.screen_dict.values()).index(self.stack.currentIndex())]))
        self.show_target_screen(target="Crash")

    # Method to call once updates have been checked to resize and start the main program
    def load_complete(self, current_version):
        self.current_version = current_version
        self.bb.logger.info("")
        
        # Set the main window title
        self.setWindowTitle("{} {}".format(self.program_title, self.current_version))

        # Update the current version for the feeback screen
        self.feedback_screen.update_current_version(current_version=current_version)

        # Set the window size and screen
        self.resize(self.main_screen.availableGeometry().size())
        self.showMaximized()
        self.show_target_screen(target=self.default_screen_name)
        self.loading_screen.close()
        self.show()

    # Method to center the main window in the screen
    def center(self):
        # Center the widget in the screen 
        self.setGeometry(QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight, 
            Qt.AlignmentFlag.AlignCenter, 
            self.size(),
            self.screen().availableGeometry()
        ))
    
    # Method to overide a window close command
    def closeEvent(self, *args, **kwargs):
        self.bb.logger.info("Window exited by user")
        if self.stack.currentIndex() == self.screen_dict["Crash"]:
            self.crash_screen.post_crash_log()
        
        super(QMainWindow, self).closeEvent(*args, **kwargs)


