import os
import win32api
import win32security
import pywin32

def encrypt_file(file_path):
    file_attributes = win32api.GetFileAttributes(file_path)
    win32api.SetFileAttributes(file_path, win32file.FILE_ATTRIBUTE_NORMAL)
    win32file.EncryptFile(file_path)
    win32api.SetFileAttributes(file_path, file_attributes)

def encrypt_files_in_folder(folder_path):
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            encrypt_file(file_path)

folder_path = "D:\downloads"
encrypt_files_in_folder(folder_path)
