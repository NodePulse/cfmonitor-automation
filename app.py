# app.py

from flask import Flask, request, render_template, send_from_directory, url_for
import os
from ai_agent import config
from ai_agent.processor import process_docx_file, export_problems_to_csv
from ai_agent.utils import ensure_dirs

app = Flask(__name__)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["RESULTS_FOLDER"], exist_ok=True)

ensure_dirs()


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/results/<filename>")
def download_file(filename):
    return send_from_directory(
        app.config["RESULTS_FOLDER"], filename, as_attachment=True
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return render_template("upload.html", message="No file part")

    file = request.files["file"]
    week = int(request.form.get("week", 1))
    level = int(request.form.get("level", 1))

    if file.filename == "":
        return render_template("upload.html", message="No selected file")

    if not file.filename.lower().endswith(".docx"):
        return render_template("upload.html", message="Only .docx files allowed")

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)
    print(f"Uploaded file saved to: {file_path}")

    # Process and export
    problems = process_docx_file(file_path, week, level)
    csv_path = export_problems_to_csv(
        problems, file.filename, app.config["RESULTS_FOLDER"]
    )
    csv_filename = os.path.basename(csv_path)

    return render_template(
        "upload.html",
        message=f"File processed. CSV saved to: {csv_path}",
        download_link=url_for("download_file", filename=csv_filename),
    )


if __name__ == "__main__":
    app.run(debug=True)
