import json, os, sys, subprocess

from PyQt6.QtWidgets import QDialog, QGridLayout, QStyle, QSizePolicy, QFileDialog
from PyQt6.QtCore import Qt

from apsfuncs.GUI.BaseWidgets import Label, PushButton
from apsfuncs.GUI.StyleSheets.TitleThemeHandling import TitleThemeManager

from apsfuncs.Toolbox.UpdateAuthentication import TokenAuthenticator
from apsfuncs.Toolbox.ConfigHandlers import get_resource_path
from apsfuncs.Toolbox.GlobalTools import BlackBoard

# Info dialog to tell the user a pop up message
class InfoDialog(QDialog):
    # Init
    def __init__(self, msg):
        super().__init__()
        
        # Set the window data
        self.setWindowTitle("INFO")

        # Create a label for the current loading text 
        load_label = Label(start_text=msg)
        load_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Create a pair of buttons for accepting or rejecting the update
        close_button = PushButton(button_text="Confirm")
        close_button.clicked.connect(self.close_dialog)

        # Create the dialog layout
        main_layout =  QGridLayout()

        # Add the widget contents to the layout
        main_layout.addWidget(load_label, 0, 0, 1, 1)
        main_layout.addWidget(close_button, 1, 0, 1, 1)

        # Add the layout to the widget and center the widget
        self.setLayout(main_layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
    # Hook to show event to add the window to the title theme manager
    def showEvent(self, e):
        super().showEvent(e)
        TitleThemeManager.instance().register_window(self)

    # Function to close the message dialog
    def close_dialog(self):
        self.close()

# Custom dialog for loading
class UpdateDialog(QDialog):
    # Init
    def __init__(self, new_version, new_version_url, updater_name, prog_name):
        super().__init__()
        self.new_version = new_version
        self.updater_name = updater_name
        self.prog_name = prog_name
        self.new_version_url = new_version_url

        # Set up class reference to global black board
        self.bb = BlackBoard.instance()
        
        # Set the window data
        self.setWindowTitle("Update system")

        # Create a label for the current loading text 
        load_label = Label(start_text="Version {} is now available, would you like to update?".format(self.new_version))

        # Create a pair of buttons for accepting or rejecting the update
        accept_button = PushButton(button_text="Update")
        accept_button.clicked.connect(self.update_version)
        reject_button = PushButton(button_text="Maybe later")
        reject_button.clicked.connect(self.maintain_version)

        # Create the dialog layout
        main_layout =  QGridLayout()

        # Add the widget contents to the layout
        main_layout.addWidget(load_label, 0, 0, 1, 2)
        main_layout.addWidget(accept_button, 1, 0, 1, 1)
        main_layout.addWidget(reject_button, 1, 1, 1, 1)

        # Add the layout to the widget and center the widget
        self.setLayout(main_layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
    # Hook to show event to add the window to the title theme manager
    def showEvent(self, e):
        super().showEvent(e)
        TitleThemeManager.instance().register_window(self)

    # Method to call update software and update the program
    def update_version(self):
        self.bb.logger.info("Updating program being run for version {}".format(self.new_version))

        # Get the location of the updater executable
        updater_filename = self.updater_name + '.exe'
        updater_file_loc = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), updater_filename)

        # Check that the updater file location exists, if not then request that the user select the correct path
        if not os.path.exists(updater_file_loc):
            self.bb.logger.info("Updater file has not been found, requesting file selection from user")

            # Show the user an explanation dialog
            info_popup = InfoDialog(msg="Updater program could not be found (this may be due to an old software verison) \nplease select the updater program to use")
            info_popup.exec()

            updater_file_loc = QFileDialog.getOpenFileName(None, caption="Select updater program", filter="*.exe", directory=os.path.dirname(os.path.abspath(sys.argv[0])))[0]
            self.bb.logger.info("User selected file {}".format(updater_file_loc))

            # Check that the new file is not empty and exists#
            if len(updater_file_loc)<2 or not os.path.exists(updater_file_loc):
                # The selected file does not exist, log it and tell the user
                self.bb.logger.info("User selection was not valid")
                info_popup = InfoDialog(msg="The selected program was not valid, the update will be postphoned")
                info_popup.exec()

        # Call the updater with all needed arguments to update
        self.bb.logger.info("Looking for updater at {}".format(updater_file_loc))
        self.bb.logger.info("Calling update program with target url: {}".format(self.new_version_url))

        # Get the current program filepath
        prog_path = sys.executable

        # Pass all needed data to the updater (the updater, the target version number, url for the release and the path of the current program)
        subprocess.Popen([updater_file_loc, "#TarVerNum", self.new_version, "#TarVerURL", self.new_version_url, "#ProgPath", prog_path])

        # Close the dialog, log and program
        self.close()
        self.bb.logger.info("Log closed")
        sys.exit()

    # Method to maintain teh current version and continue with the program
    def maintain_version(self):
        self.close()
        
        
    # Method to center the dialog in the screen
    def center(self):
        # Center the widget in the screen 
        self.setGeometry(QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight, 
            Qt.AlignmentFlag.AlignCenter, 
            self.size(),
            self.screen().availableGeometry()
        ))

# Function to return if there is a newer program version available
def check_for_avaiable_update(server_auth_location, use_dev=False):

    # Set up class reference to global black board
    bb = BlackBoard.instance()

    # Open the version data file and retrieve the version information
    version_file_loc = os.path.join(get_resource_path(), 'version.json')
    with open(version_file_loc) as version_json_data:
        app_version_data = json.load(version_json_data)
        version_json_data.close()

    # Set up an authenticator
    authenticator = TokenAuthenticator(server_auth_location=server_auth_location)

    # Get a list of releases from the repo
    token_source, release_response = authenticator.get_releases(url=app_version_data['RepoPath'])
    bb.logger.info("Using the {} token".format(token_source))

    if release_response.ok:
        releases = release_response.json()
    else:
        bb.logger.info("Failed to get any releases")
        releases = []

    # Get the current version of the program and set it as the latest
    latest_version = app_version_data['Version'][1:]
    latest_release = None

    # For each release found in the repo, check if it is newwer than the current, if so then replace the latest version
    for release in releases:
        latest_version_split = latest_version.split(".")
        # Check if the release is pre-release, if so then only add it if use_dev is true
        if release['prerelease'] and not use_dev:
            continue

        # Compare the release version with the current latest vesion
        available_verison = release['tag_name'][1:]
        available_verison_split = available_verison.split(".")
        if int(latest_version_split[0]) < int(available_verison_split[0]):
            # There is a newer major version
            latest_version = available_verison
            latest_release = release
            continue
        elif int(latest_version_split[1]) < int(available_verison_split[1]) and int(latest_version_split[0]) == int(available_verison_split[0]):
            # The major version is the same, and there is a newer minor version
            latest_version = available_verison
            latest_release = release
            continue
        elif int(latest_version_split[2]) < int(available_verison_split[2])and int(latest_version_split[1]) == int(available_verison_split[1]) and int(latest_version_split[0]) == int(available_verison_split[0]):
            # The major version is the same, as is the minor version and there is a newer patch version
            latest_version = available_verison
            latest_release = release
            continue
    
    # Confirm if the current version is the latest version
    if latest_version == app_version_data['Version'][1:]:
        update_available = False
        latest_version_url = ""
        bb.logger.info("Running latest version")
    else:
        update_available = True
        latest_version_url = latest_release['url']
        bb.logger.info("new version {} found".format(latest_version))


    # Return the found information: If a release is avaiable, the current version number, new latest version number, url for latest release, and the updater executable name
    return update_available, app_version_data['Version'], latest_version, latest_version_url, app_version_data['UpdaterName'], app_version_data["ProgramName"]

# Function to check for updates and ask the user if they want to update etc. Also pass back the current program version
def handle_auto_update():

    # Set up class reference to global black board
    bb = BlackBoard.instance()
    
    # Check for an update
    bb.logger.info("Checking for updates")
    return check_for_avaiable_update(use_dev=bb.config_dict['Use_dev'], server_auth_location=bb.config_dict["Server_auth_location"])