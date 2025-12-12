import os
import json

from PyQt6.QtWidgets import QWidget, QGridLayout, QDialog, QSizePolicy, QFileDialog
from PyQt6.QtCore import Qt

from apsfuncs.GUI.BaseWidgets import PushButton, CheckBox, Label
from apsfuncs.GUI.StyleSheets.TitleThemeHandling import TitleThemeManager
from apsfuncs.Toolbox.ConfigHandlers import get_resource_path, update_saved_config_dict
from apsfuncs.Toolbox.GlobalTools import BlackBoard

# Custom dialog for confirming resetting to default settings
class ResetSettingsConfDialog(QDialog):
    # Init
    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        
        # Set up class reference to global black board
        self.bb = BlackBoard.instance()
        
        # Set the window data
        self.setWindowTitle("Reset to default settings")

        # Create a label for the current loading text 
        info_label = Label(start_text="Are you sure you want to reset to default settings? This cannot be undone")

        # Create a pair of buttons for accepting or rejecting the update
        accept_button = PushButton(button_text="Confirm")
        accept_button.clicked.connect(self.confirm_reset)
        reject_button = PushButton(button_text="Cancel")
        reject_button.clicked.connect(lambda: self.close())

        # Create the dialog layout
        main_layout =  QGridLayout()

        # Add the widget contents to the layout
        main_layout.addWidget(info_label, 0, 0, 1, 2)
        main_layout.addWidget(accept_button, 1, 0, 1, 1)
        main_layout.addWidget(reject_button, 1, 1, 1, 1)

        # Add the layout to the widget and center the widget
        self.setLayout(main_layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
    # Hook to show event to add the window to the title theme manager
    def showEvent(self, e):
        super().showEvent(e)
        TitleThemeManager.instance().register_window(self)

    # Method to confirm a setting reset
    def confirm_reset(self):
        # Call the parent reset and close the dialog
        self.bb.logger.info("Reset settings confirmed by user")
        self.parent_widget.reset_config()
        self.close()

# Custom dialog for saving setting changes
class SaveChangesDialog(QDialog):
    # Init
    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget

        # Set up class reference to global black board
        self.bb = BlackBoard.instance()
        
        # Set the window data
        self.setWindowTitle("Save changes")

        # Create a label for the current loading text 
        info_label = Label(start_text="Do you want to save your changes?")

        # Create a pair of buttons for accepting or rejecting the update
        accept_button = PushButton(button_text="Confirm")
        accept_button.clicked.connect(self.confirm_save)
        reject_button = PushButton(button_text="Discard")
        reject_button.clicked.connect(lambda: self.close())

        # Create the dialog layout
        main_layout =  QGridLayout()

        # Add the widget contents to the layout
        main_layout.addWidget(info_label, 0, 0, 1, 2)
        main_layout.addWidget(accept_button, 1, 0, 1, 1)
        main_layout.addWidget(reject_button, 1, 1, 1, 1)

        # Add the layout to the widget and center the widget
        self.setLayout(main_layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
    
    # Hook to show event to add the window to the title theme manager
    def showEvent(self, e):
        super().showEvent(e)
        TitleThemeManager.instance().register_window(self)

    # Method to confirm a setting reset
    def confirm_save(self):
        # Call the parent reset and close the dialog
        self.bb.logger.info("Save changes confirmed by user")
        self.parent_widget.update_config_json()
        self.close()

# Class to hold a settings screen for config settings and a feedback option
class SettingsScreenAPSBase(QWidget):

    # Init
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Set up class reference to global black board
        self.bb = BlackBoard.instance()

        # Create a holding settings dictionary to hold changes before they are confirmed on leaving the page
        self.holding_dict = None

        # Create button to return
        back_button = PushButton(button_text="Return")
        back_button.clicked.connect(self.return_clicked)

        # Create a checkbox and label for opting in to alpha releases
        self.alpha_opt_in_box = CheckBox()
        self.alpha_opt_in_box.stateChanged.connect(self.update_alpha_opt_in)
        alpha_opt_in_label = Label(start_text="Use alpa versions of the software (WARNING these may be unstable or have bugs or crashes)")

        # Create a checkbox and label for maintaining config options over an update
        self.maintain_config_box = CheckBox()
        self.maintain_config_box.stateChanged.connect(self.update_maintain_config)
        maintain_config_label = Label(start_text="Keep settings when an update is carried out")

        # Create a label and button for the crash og repo
        self.crash_repo_label = Label(start_text="Unloaded")
        self.crash_repo_button = PushButton(button_text="Select new location")
        self.crash_repo_button.clicked.connect(self.update_crash_repo_location)

        # Create a label and button for the crash og repo
        self.feedback_repo_label = Label(start_text="Unloaded")
        self.feedback_repo_button = PushButton(button_text="Select new location")
        self.feedback_repo_button.clicked.connect(self.update_feedback_repo_location)

        # Create a label and button for the crash og repo
        self.server_auth_repo_label = Label(start_text="Unloaded")
        self.server_auth_repo_button = PushButton(button_text="Select new location")
        self.server_auth_repo_button.clicked.connect(self.update_server_auth_repo_location)

        # Add a button to return the config settings to their default values
        reset_config_button = PushButton(button_text="Reset to defaults")
        reset_config_button.clicked.connect(self.confirm_reset_config)

        # Create thee scene layout and add the base content to it
        base_conent_layout = QGridLayout()

        # Add the content to the layout
        base_conent_layout.addWidget(alpha_opt_in_label, 0, 0, 1, 1)
        base_conent_layout.addWidget(self.alpha_opt_in_box, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter)

        base_conent_layout.addWidget(maintain_config_label, 1, 0, 1, 1)
        base_conent_layout.addWidget(self.maintain_config_box, 1, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter)

        base_conent_layout.addWidget(self.crash_repo_label, 2, 0, 1, 1)
        base_conent_layout.addWidget(self.crash_repo_button, 2, 1, 1, 1)

        base_conent_layout.addWidget(self.feedback_repo_label, 3, 0, 1, 1)
        base_conent_layout.addWidget(self.feedback_repo_button, 3, 1, 1, 1)

        base_conent_layout.addWidget(self.server_auth_repo_label, 4, 0, 1, 1)
        base_conent_layout.addWidget(self.server_auth_repo_button, 4, 1, 1, 1)

        base_conent_layout.addWidget(reset_config_button, 8, 0, 1, 2)
        base_conent_layout.addWidget(back_button, 9, 0, 1, 2)

        # Put the base conent into a widget that can be inehrited by a child screen
        self.base_content = QWidget()
        self.base_content.setLayout(base_conent_layout)
    
    # Method to grab the return clicked before passing it to the main window
    def return_clicked(self):
        # Check if any of the held config settigns are differnet to the config dict values
        if self.holding_dict != self.bb.config_dict:
            self.bb.logger.info("Setting changes detected")

            # Show confirmation dialog to confirm if the user wants to save their changes
            conf_dialog = SaveChangesDialog(parent_widget=self)
            conf_dialog.exec()
            self.bb.logger.info("Save change dialog closed")

        # Pass the return command back to the main window
        self.main_window.show_previous_screen()

    # Method to resize the frame contents
    def adjust_spacing(self):
        # Calcualte the margin spacings and set the contenets margins
        width_spacing = int(self.screen().size().width() * 0.25)
        height_spacing = int(self.screen().size().height() * 0.25)
        self.setContentsMargins(width_spacing, height_spacing, width_spacing, height_spacing)
        
    # Method to call updates on the scene being re-opened
    def scene_opened(self):
        # update the displayed settings to the loaded config dict
        self.refresh_displayed_settings()

        # Store the current config dict values into the holding dictionary (copy to avoid referencing origional values)
        self.holding_dict = self.bb.config_dict.copy()
        self.bb.logger.info("Current settings stored")

    # Method to update the opt in option for alpha releases
    def update_alpha_opt_in(self, new_state):
        # Get the bool state of the checkbox 
        bool_state = self.alpha_opt_in_box.isChecked()

        # Check if the new state is differnt to the read config dict, if no then return
        if bool_state == self.holding_dict["Use_dev"]:
            return
        
        # Update the opt in option in the config dict
        self.holding_dict["Use_dev"] = bool_state
        self.bb.logger.info("Alpha opt in updated to {}".format(bool_state))

    # Method to update the maintain config over updates option
    def update_maintain_config(self, new_state):
        # Get the bool state of the checkbox 
        bool_state = self.maintain_config_box.isChecked()

        # Check if the new state is differnt to the read config dict, if no then return
        if bool_state == self.holding_dict["Keep_config"]:
            return
        
        # Update the opt in option in the config dict
        self.holding_dict["Keep_config"] = bool_state
        self.bb.logger.info("Maintain config updated to {}".format(bool_state))

    # Method to update the crash repo location
    def update_crash_repo_location(self):
        # Get a new location from the user
        new_location = QFileDialog.getExistingDirectory(None, caption="Crash repo directory", directory=self.holding_dict["Crash_log_repo"])
        if len(new_location) > 0:
            self.bb.logger.info("Crash repo location updated to {}".format(new_location))
            self.holding_dict["Crash_log_repo"] = new_location
        else:
            # No folder was selected
            return
        # Update the crash repo label to the new location
        self.crash_repo_label.setText("Crash repo location: {}".format(self.holding_dict["Crash_log_repo"]))

    # Method to update the feedback repo location
    def update_feedback_repo_location(self):
        # Get a new location from the user
        new_location = QFileDialog.getExistingDirectory(None, caption="Feedback repo directory", directory=self.holding_dict["Feedback_repo"])
        if len(new_location) > 0:
            self.bb.logger.info("Feedback repo location updated to {}".format(new_location))
            self.holding_dict["Feedback_repo"] = new_location
        else:
            # No folder was selected
            return
        # Update the feedback repo label to the new location
        self.feedback_repo_label.setText("Feedback repo location: {}".format(self.holding_dict["Feedback_repo"]))

    # Method to update the server auth repo location
    def update_server_auth_repo_location(self):
        # Get a new location from the user
        new_location = QFileDialog.getOpenFileName(None, caption="Server auth file", directory=os.path.dirname(self.holding_dict["Server_auth_location"]), filter='*.json')[0]
        if len(new_location) > 4:
            self.bb.logger.info("Server auth location updated to {}".format(new_location))
            self.holding_dict["Server_auth_location"] = new_location
        else:
            # No folder was selected
            return
        # Update the server auth repo label to the new location
        self.server_auth_repo_label.setText("Server auth location: {}".format(self.holding_dict["Server_auth_location"]))

    # Method to create confirm dialog on reset config settings option
    def confirm_reset_config(self):
        self.bb.logger.info("Reset to deaults selected")
        # Create and open a confirmation dialog
        conf_dialog = ResetSettingsConfDialog(parent_widget=self)
        conf_dialog.exec()
        self.bb.logger.info("Reset setting dialg closed")

    # Method to reset the config settings to their default values
    def reset_config(self):

        # Load in the default config dictionary
        default_config_file_loc = os.path.join(get_resource_path(), "default_config.json")
        with open(default_config_file_loc) as config_file:

            # Overwrite the config dict with the default values
            self.bb.config_dict = json.load(config_file)
        self.bb.logger.info("Config settings read from defualt config")

        # Trigger the refresh methods as if the screen was re-opened
        self.scene_opened()

        # Update the config json to write the default values back into the config file
        self.update_config_json()


    # Method to overrite the config.json file with the current read in dictionary
    def update_config_json(self):
        update_saved_config_dict(self.holding_dict)
        self.bb.logger.info("Holding dictionary dumped to config.json")

        # Set the config dictionary to the holding dictionary values, without removing the shared pointer through the rest of the program
        for key in self.bb.config_dict.keys():
            if key in self.holding_dict:
                self.bb.config_dict[key] = self.holding_dict[key]

        # Call the main window config change listener
        self.main_window.call_config_change_listeners()
    
    # Method to set the display options to the current config settigns
    def refresh_base_aps_settings(self):

        # Update the alpha opt in checkbox
        self.alpha_opt_in_box.blockSignals(True)
        self.alpha_opt_in_box.setChecked(self.bb.config_dict["Use_dev"])
        self.alpha_opt_in_box.blockSignals(False)
        
        # Update the maintain config checkbox
        self.maintain_config_box.blockSignals(True)
        self.maintain_config_box.setChecked(self.bb.config_dict["Keep_config"])
        self.maintain_config_box.blockSignals(False)

        # Update the crash repo location labels
        self.crash_repo_label.setText("Crash repo location: {}".format(self.bb.config_dict["Crash_log_repo"]))
        self.feedback_repo_label.setText("Feedback repo location: {}".format(self.bb.config_dict["Feedback_repo"]))
        self.server_auth_repo_label.setText("Server auth location: {}".format(self.bb.config_dict["Server_auth_location"]))
