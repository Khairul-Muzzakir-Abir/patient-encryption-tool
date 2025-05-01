import os
from datetime import datetime
from utils import generate_key, load_key, encrypt_file, decrypt_file
import shutil

# Ensure key exists
if not os.path.exists("secret.key"):
    generate_key()
key = load_key()

# Directories
input_folder = "patient_data/"
encrypted_folder = "encrypted_data/"
decrypted_folder = "patient_data_decrypted/"

# Create output folder if it doesn't exist
if not os.path.exists(encrypted_folder):
    os.makedirs(encrypted_folder)
if not os.path.exists(decrypted_folder):
    os.makedirs(decrypted_folder)

# Encrypt all files in the patient_data/ folder
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    if os.path.isfile(file_path):  # Ensure it's a file
        encrypted_file = os.path.join(encrypted_folder, f"{filename}.enc")
        encrypt_file(file_path, encrypted_file, key)
        print(f"🔐 Encrypted {file_path} → {encrypted_file}")

# Ask for password BEFORE decrypting
password = input("Enter password to decrypt: ")
if password != "mypassword123":
    print("❌ Incorrect password. Decryption aborted.")
    exit()

# Decrypt all encrypted files in the encrypted_data/ folder
for filename in os.listdir(encrypted_folder):
    file_path = os.path.join(encrypted_folder, filename)
    if os.path.isfile(file_path):  # Ensure it's a file
        decrypted_file = os.path.join(decrypted_folder, filename.replace(".enc", "_decrypted.csv"))
        decrypt_file(file_path, decrypted_file, key)
        print(f"🔓 Decrypted {file_path} → {decrypted_file}")

# Log activity
with open("logs/access_log.txt", "a") as log:
    log.write(f"{datetime.now()}: Encrypted and decrypted all patient files\n")

# Create timestamped backup for each encrypted file
for filename in os.listdir(encrypted_folder):
    file_path = os.path.join(encrypted_folder, filename)
    if os.path.isfile(file_path):  # Ensure it's a file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup/{filename.replace('.enc', f'_{timestamp}.enc')}"
        shutil.copy2(file_path, backup_filename)
        print(f"📁 Backup created: {backup_filename}")

        # Log the backup
        with open("logs/access_log.txt", "a") as log:
            log.write(f"{datetime.now()}: Backup created at {backup_filename}\n")
