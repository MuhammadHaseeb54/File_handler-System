import zipfile
import os

upload_folder = 'uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
def zip_files(file_paths, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    zipf.write(file_path, os.path.basename(file_path))  # Add file with its basename
                except Exception as e:
                    print(f"Error adding {file_path} to zip: {e}")
            else:
                print(f"File {file_path} does not exist.")


def unzip_files(zip_file, extract_to):
    
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        zipf.extractall(extract_to)
