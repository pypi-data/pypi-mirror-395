import os, shutil

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QStyle
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QThread, Qt, QRect

from apsfuncs.GUI.BaseWidgets import Label
from apsfuncs.Toolbox.TemplateThreading import UpdateThreadWorker, LoadingThread
from apsfuncs.Toolbox.AutoUpdating import UpdateDialog
from apsfuncs.Toolbox.ConfigHandlers import get_resource_path, get_crash_log_path, get_held_feedback_path
from apsfuncs.Toolbox.GlobalTools import BlackBoard

# Define the loading screen
class LoadingScreen(QWidget):
    
    # Init class
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Set up class reference to global black board
        self.bb = BlackBoard.instance()
        
        # Set the window title
        self.setWindowTitle("Loading...")
        self.setFixedSize(192, 192)

        # Load in the animation sprite map and detect the number of images
        self.animation_sprite_sheet = QPixmap(os.path.join(get_resource_path(), "LoadingFrames", 'loading_spritesheet.png'))
        self.sprite_height = 192
        self.sprite_width = 192
        self.sprite_columns = self.animation_sprite_sheet.size().width() / self.sprite_width
        self.sprit_rows = self.animation_sprite_sheet.size().height() / self.sprite_height

        self.loaded_sprite_index = [0,0]
        loaded_sprite_rect = QRect(self.loaded_sprite_index[0]*self.sprite_width, self.loaded_sprite_index[1]*self.sprite_height, self.sprite_width, self.sprite_height)
        loaded_sprite_img = self.animation_sprite_sheet.copy(loaded_sprite_rect)
        
        self.display_label = Label()
        self.display_label.setPixmap(loaded_sprite_img)
        self.display_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.display_label.setFixedSize(loaded_sprite_img.size())  # Lock label to image size
        loading_layout = QVBoxLayout()
        loading_layout.setContentsMargins(0, 0, 0, 0)
        loading_layout.addWidget(self.display_label)
        self.setLayout(loading_layout)

        self.adjustSize() 
        self.center()
        self.show()

        # Check for held files to move to the external repo
        self.bb.logger.info("Checcking for held crash logs")
        self.check_for_held_files(file_type="crash logs", folder_path=get_crash_log_path(), external_repo=self.bb.config_dict["Crash_log_repo"])
        self.bb.logger.info("Checcking for held feedback files")
        self.check_for_held_files(file_type="feedback files", folder_path=get_held_feedback_path(), external_repo=self.bb.config_dict["Feedback_repo"])

        # Check for software updates
        self.bb.logger.info("Checcking for available updates")
        self.check_for_updates()

    # Define a mehtod to check for held crash logs or feedback respones
    def check_for_held_files(self, file_type, folder_path, external_repo):

        # Check if there are any held files in the target folder path, if there are then try to move them to the external repo
        if os.path.exists(folder_path):
            file_list = os.listdir(folder_path)
            if len(file_list) > 0:
                self.bb.logger.info("Held {} have been found, trying to move them to external repo".format(file_type))
                for file in file_list:
                    try:
                        # Try to put the file in the external crash repo
                        src_file = os.path.join(folder_path, file)
                        remote_dst_file = os.path.join(external_repo, file)
                        shutil.copyfile(src=src_file, dst=remote_dst_file)

                        # Remove the log file from the held crash logs
                        os.remove(src_file)
                        self.bb.logger.info("{} has been moved sucessfully".format(file))

                    except Exception as e:
                        self.bb.logger.exception("Failed to move {} into external repo, error {}".format(file, e))

    # Define function to handle updating
    def check_for_updates(self):

        # Create a thread for the loading gui loop
        self.dynamic_time_thread = QThread()
        self.dynamic_time_worker = LoadingThread()
        self.dynamic_time_worker.moveToThread(self.dynamic_time_thread)

        self.dynamic_time_thread.started.connect(self.dynamic_time_worker.run)
        self.dynamic_time_worker.loading_tick.connect(self.tick_animation)

        # Add closing links from the update worker 
        self.dynamic_time_worker.finished.connect(self.dynamic_time_thread.quit)
        self.dynamic_time_worker.finished.connect(self.dynamic_time_worker.deleteLater)
        self.dynamic_time_thread.finished.connect(self.dynamic_time_thread.deleteLater)
        
        # Create a thread to handle auto update loading
        self.update_thread = QThread()
        self.update_worker = UpdateThreadWorker()
        self.update_worker.moveToThread(self.update_thread)

        self.update_thread.started.connect(self.update_worker.run)
        self.update_worker.update_check_complete.connect(self.load_complete)
        self.update_worker.update_check_complete.connect(self.dynamic_time_worker.stop)

        self.update_worker.update_check_complete.connect(self.update_thread.quit)
        self.update_worker.update_check_complete.connect(self.update_worker.deleteLater)
        self.update_thread.finished.connect(self.update_thread.deleteLater)

        # Start the auto updater thread
        self.update_thread.start()
        self.bb.logger.info("Updater thread started")

        # Start the auto updater thread
        self.dynamic_time_thread.start()
        self.bb.logger.info("Dynamic load timer started")

    # Define method to call the main window load complete method
    def load_complete(self, update_data):
        update_available = update_data[0]
        current_version = update_data[1]
        latest_version = update_data[2]
        latest_version_url = update_data[3]
        updater_name = update_data[4]  
        prog_name = update_data[5]  
        
        self.bb.logger.info("Auto update check complete")
        # If an update is avaiable then ask the user if they want to update

        if update_available:    
            # If an update is available, start a dialog box to ask the user if they would like to auto update
            update_dialog = UpdateDialog(new_version=latest_version, new_version_url=latest_version_url, updater_name=updater_name, prog_name=prog_name)
            update_dialog.exec()
        else:
            # Otherwise just start the main program
            self.bb.logger.info("Running the latest version")
        self.main_window.load_complete(current_version=current_version)

    # Define the animation method
    def tick_animation(self):
        # Update the loaded sprite index
        if self.loaded_sprite_index[0] < self.sprite_columns-1:
            # There is another sprite in the current row so move to it
            self.loaded_sprite_index[0] += 1
        elif self.loaded_sprite_index[1] < self.sprite_columns-1:
            # There was not another sprite in the current row but there is another row so start that row from 0
            self.loaded_sprite_index[1] += 1 
            self.loaded_sprite_index[0] = 0
        else:
            # There were no more image rows or column so start again
            self.loaded_sprite_index = [0,0]

        # Get the sprite from the sprite map
        loaded_sprite_rect = QRect(self.loaded_sprite_index[0]*self.sprite_width, self.loaded_sprite_index[1]*self.sprite_height, self.sprite_width, self.sprite_height)
        loaded_sprite_img = self.animation_sprite_sheet.copy(loaded_sprite_rect)

        # Update the display
        self.display_label.setPixmap(loaded_sprite_img)
        

    # Method to center the main window in the screen
    def center(self):
        # Center the widget in the screen 
        self.setGeometry(QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight, 
            Qt.AlignmentFlag.AlignCenter, 
            self.size(),
            self.screen().availableGeometry()
        ))

        