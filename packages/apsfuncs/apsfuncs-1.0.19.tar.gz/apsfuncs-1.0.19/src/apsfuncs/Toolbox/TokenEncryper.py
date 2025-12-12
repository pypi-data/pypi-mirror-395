from cryptography.fernet import Fernet

# function to print a key and encrypted token from a passed raw token 

def encrypt_token(token=""):
    # Generate encryption key
    key = Fernet.generate_key()
    cipher = Fernet(key)

    encrypted_token = cipher.encrypt(token.encode())

    print("Key: {}".format(key.decode()))
    print("Encrypted token: {}".format(encrypted_token.decode()))