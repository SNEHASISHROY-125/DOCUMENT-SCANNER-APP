'''
AUTO GENERATE ZIP FILE
'''

import os
import shutil
from zipfile import ZipFile

def move_files_and_zip(source_folder, destination_folder, zip_file_name):
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Move files from source_folder to destination_folder
    for file_name in os.listdir(source_folder):
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)
        shutil.move(source_path, destination_path)

    # Create a zip file of the destination folder
    with ZipFile(zip_file_name, 'w') as zip_file:
        for folder_name, subfolders, file_names in os.walk(destination_folder):
            for file_name in file_names:
                file_path = os.path.join(folder_name, file_name)
                arcname = os.path.relpath(file_path, destination_folder)
                zip_file.write(file_path, arcname=arcname)

    print(f"Files moved to {destination_folder} and zipped as {zip_file_name}")

################################################################################

# Replace these values with your actual paths and file names
source_folder = "./source"
destination_folder = "./destination"
zip_file_name = "output.zip"

move_files_and_zip(source_folder, destination_folder, zip_file_name)
