import os, sys, json, requests

from cryptography.fernet import Fernet
from apsfuncs.Toolbox.ConfigHandlers import get_resource_path

# Class to hold authentication handling for updating requests
class TokenAuthenticator:
    # Init
    def __init__(self, server_auth_location):
        self.server_auth_location = server_auth_location
        self.token = self.load_token()

    # Function to attempt to load from a recovery token
    def recover_token(self):
        # Open the json from the executable directory (if a recovery token is placed in the working folder) location
        recovery_auth_loc = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "recovery_auth.json")

        # Check the program has access to the file, if not then just return a none tocken
        if not os.path.exists(recovery_auth_loc):
            return None
        
        with open(recovery_auth_loc) as recovery_auth_file:
            recovery_auth_json = json.load(recovery_auth_file)

        key = recovery_auth_json['AuthKey']
        cipher = Fernet(key)
        encrypted_token = recovery_auth_json['EncryptedToken']

        # Try to decode the found token with the found key
        try:
            token = cipher.decrypt(encrypted_token).decode()
            return token
        except:
            # Bad token info
            return None

    # Function to return the stored PAT token
    def load_token(self):
        # Get the enctryption key from the local file storage
        auth_key_json_loc = os.path.join(get_resource_path(), "auth_key.json")
        with open(auth_key_json_loc) as auth_key_file:
            auth_key_json = json.load(auth_key_file)

            auth_key = auth_key_json['AuthKey']
            cipher = Fernet(auth_key)
        
        # Get the enctrypted token from the server location
        # Check the program has access to the file, if not then just return none 
        if not os.path.exists(self.server_auth_location):
            return self.recover_token()
        
        with open(self.server_auth_location) as token_file:
            token_json = json.load(token_file)

        encrypted_token = token_json['EncryptedToken']

        # Try to decode the found token with the found key
        try:
            token = cipher.decrypt(encrypted_token).decode()
            return token
        except:
            # Bad token info
            return self.recover_token()
            
    # Function to return the current releases
    def get_releases(self, url):
        # If no token was accessable, then return a failed response
        if self.token is None:
            return "none", requests.get(url=url)
        
        # Try to make the request with the stored token
        headers = {
            "Authorization": "token {}".format(self.token), 
            "Accept": "application/vnd.github.v3+json"
        }
        return "confirmed", requests.get(url=url, headers=headers)
    
    # Function to get a download
    def get_download(self, url):
        # If no token was accessable, then return a failed response
        if self.token is None:
            return "none", requests.get(url=url)
        # Otherwise return the download using the token
        headers = {
            "Authorization": "token {}".format(self.token), 
            "Accept": "application/octet-stream"
        }
        return requests.get(url=url, headers=headers)