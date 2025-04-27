from flask import Flask, redirect, render_template, request, send_file
import os
import glob
import zipfile
from werkzeug.utils import secure_filename
import file_operations  
import file_handling

app = Flask(__name__)

app.config["FILE_UPLOADS"] = "D:/FILE_ZIPPER/uploads"
app.config["FILE_DOWNLOADS"] = "D:/FILE ZIPPER/downloads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

os.makedirs(app.config["FILE_UPLOADS"], exist_ok=True)
os.makedirs(app.config["FILE_DOWNLOADS"], exist_ok=True)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"txt", "pdf", "docx", "csv", "zip"}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_large_file(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        for chunk in uploaded_file.stream:
            f.write(chunk)

@app.route("/")
def home():
    # Clear upload and download folders on app startup
    for folder in [app.config["FILE_UPLOADS"], app.config["FILE_DOWNLOADS"]]:
        for f in os.listdir(folder):
            file_path = os.path.join(folder, f)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
    return render_template("home.html")

@app.route("/compress", methods=["GET", "POST"])
def compress_route():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        uploaded_file = request.files["file"]
        if uploaded_file.filename == "" or not allowed_file(uploaded_file.filename):
            return redirect(request.url)

        if uploaded_file:
            file_path = os.path.join(app.config["FILE_UPLOADS"], secure_filename(uploaded_file.filename))
            uploaded_file.save(file_path)

        try:
            compressed_path = file_handling.compress(file_path)  # Modify based on your file structure
            if compressed_path and os.path.exists(compressed_path):
                return send_file(compressed_path, as_attachment=True)
        except Exception as e:
            print(f"Compression error: {e}")
            return "An error occurred during compression.", 500

    return render_template("compress.html")

@app.route("/decompress", methods=["GET", "POST"])
def decompress_route():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        uploaded_file = request.files["file"]
        if uploaded_file.filename == "" or not uploaded_file.filename.endswith(".zip"):
            return "Error: Please upload a valid .zip file.", 400

        # Save the uploaded zip file
        file_path = os.path.join(app.config["FILE_UPLOADS"], secure_filename(uploaded_file.filename))
        save_large_file(uploaded_file, file_path)

        try:
            # Decompress the file
            decompressed_dir = os.path.join(app.config["FILE_DOWNLOADS"], "decompressed_files")
            os.makedirs(decompressed_dir, exist_ok=True)

            decompressed_path = file_handling.decompress(file_path)  # Modify if the function signature differs
            if os.path.isdir(decompressed_path):
                # Compress decompressed files into a single .zip for download
                output_zip = os.path.join(app.config["FILE_DOWNLOADS"], "decompressed_archive.zip")
                with zipfile.ZipFile(output_zip, "w") as zipf:
                    for root, _, files in os.walk(decompressed_path):
                        for file in files:
                            file_full_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_full_path, decompressed_path)
                            zipf.write(file_full_path, arcname)
                return send_file(output_zip, as_attachment=True)
            elif os.path.isfile(decompressed_path):
                # If a single file is decompressed, return it directly
                return send_file(decompressed_path, as_attachment=True)
            else:
                return "Error: Unexpected decompression result.", 500

        except Exception as e:
            print(f"Decompression error: {e}")
            return "An error occurred during decompression.", 500

    return render_template("decompress.html")


@app.route("/zip", methods=["GET", "POST"])
def zip_files_route():
    if request.method == "POST":
        # Get the list of uploaded files
        uploaded_files = request.files.getlist("files")

        # Check if files are provided and valid
        if not uploaded_files or any(f.filename == "" or not allowed_file(f.filename) for f in uploaded_files):
            return "Error: Please upload valid files.", 400

        # Save uploaded files in the upload folder
        file_paths = []
        for file in uploaded_files:
            file_path = os.path.join(app.config["FILE_UPLOADS"], secure_filename(file.filename))
            save_large_file(file, file_path)
            file_paths.append(file_path)

        # Define the output ZIP file path
        output_zip = os.path.join(app.config["FILE_DOWNLOADS"], "archive.zip")

        try:
            # Compress files into a single ZIP
            zip_files(file_paths, output_zip)

            # Verify the ZIP file was created
            if os.path.exists(output_zip):
                # Send the ZIP file for download
                return send_file(output_zip, as_attachment=True)

            return "Error: Failed to create ZIP file.", 500
        except Exception as e:
            print(f"Error during zipping: {e}")
            return "An error occurred while zipping files.", 500

    return render_template("zip.html")

@app.route("/unzip", methods=["GET", "POST"])
def unzip():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        uploaded_file = request.files["file"]
        if uploaded_file.filename == "" or not uploaded_file.filename.endswith(".zip"):
            return redirect(request.url)

        file_path = os.path.join(app.config["FILE_UPLOADS"], secure_filename(uploaded_file.filename))
        save_large_file(uploaded_file, file_path)
        
        extract_to = os.path.join(app.config["FILE_DOWNLOADS"], "extracted_files")
        os.makedirs(extract_to, exist_ok=True)
        # extract_to = app.config["FILE_DOWNLOADS"]
        file_operations.unzip_files(file_path, extract_to)

        extracted_zip = os.path.join(app.config["FILE_DOWNLOADS"], "extracted_files.zip")
        file_operations.zip_files(glob.glob(os.path.join(extract_to, '*')), extracted_zip)

        return send_file(extracted_zip, as_attachment=True)

    return render_template("unzip.html")

if __name__ == "__main__":
    app.run(debug=True)


