import os
import zipfile
def read_file(file_path):
    with open(file_path, "rb") as f:
        return f.read()

def write_file(file_path, data):
    with open(file_path, "wb") as f:
        f.write(data)


def compress(input_path):
    # Add real compression logic here (e.g., zipping or Huffman encoding)
    output_path = input_path.replace(".", "-compressed.") + ".zip"
    if os.path.exists(input_path):
        # Example of real compression (using zip for simplicity)
        zip_path = input_path + ".zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(input_path, os.path.basename(input_path))
        return zip_path
    return None
def decompress(input_path):
    if os.path.exists(input_path):
        if not input_path.endswith(".zip"):
            print("Error: Input file is not a zip file.")
            return None
        try:
            # Extract files in the same directory as the zip file
            output_dir = input_path.replace(".zip", "-decompressed")
            with zipfile.ZipFile(input_path, 'r') as zipf:
                zipf.extractall(output_dir)
                print(f"Decompressed to {output_dir}")
            return output_dir
        except zipfile.BadZipFile:
            print("Error: File is not a valid zip file.")
            return None
    else:
        print("Error: Input file does not exist.")
        return None


