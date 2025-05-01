from cryptography.fernet import Fernet
import os

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as f:
        f.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_file(file_path, output_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as original_file:
        original = original_file.read()
    encrypted = f.encrypt(original)
    with open(output_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_file(file_path, output_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = f.decrypt(encrypted)
    with open(output_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted)
