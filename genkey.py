#!/usr/bin/env python3
from cryptography.fernet import Fernet

gen_key = True
gen_password = "Place your password here"

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Key file generated")

def load_key():
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open("secret.key", "rb").read()

def encode(s):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(s.encode('utf-8'))

def decode(s):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(s).decode('utf-8')

if __name__ == '__main__':
    if gen_key:
        # 1st generate the key
        generate_key()
    else:
        # 2nd encrypt the password and test it
        encrypted_message = encode(gen_password)
        print("encrypted message: {0}".format(encrypted_message))
        decrypted_message = decode(encrypted_message)
        print("dencrypted message: {0}".format(decrypted_message))
