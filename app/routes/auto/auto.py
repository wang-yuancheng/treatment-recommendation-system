from flask import Blueprint, render_template, request, url_for, redirect, flash, current_app
from werkzeug.utils import secure_filename
import pandas as pd
import os
import uuid
from app.paths import *
from model.auto_models.auto_model_train import load_dataset

# Create the Blueprint object
auto_bp = Blueprint('auto', __name__)

ALLOWED_EXTENSIONS = {'csv'}

# allowed_file(filename) returns True only if the filename contains a dot and the substring
# after the last dot (lowercased) is in the ALLOWED_EXTENSIONS whitelist
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the routes on the blueprint
@auto_bp.route('/auto', methods=["GET", "POST"])
def auto_home():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file uploaded')
            return redirect(request.url) #refreshs the page

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url) #refreshs the page

        # Proceed only if a file is provided and it has an approved CSV extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)           # Clean the filename to prevent unsafe characters or path traversal

            job_id = str(uuid.uuid4())                          # Create random UUID for each upload
            base_dir = UPLOAD_FOLDER_PATH                       # Get the upload directory path
            job_dir = os.path.join(base_dir, job_id)            # Create unique directory for each csv
            os.makedirs(job_dir, exist_ok=True)                 # Creates Upload_Folder, if already exist, continue with no error
            save_path = os.path.join(job_dir, filename)          # Build the full path where the file will be saved
            file.save(save_path)                                 # Save the uploaded file
            flash(f'File saved to {save_path}')

            # immediately load into a DataFrame
            try:
                df = load_dataset(save_path)
                flash(f"Dataset loaded: {df.shape[0]} rows × {df.shape[1]} cols")
            except Exception as e:
                flash(f"Error loading dataset: {e}", "error")

            return redirect(url_for('status.view', job_id=job_id))
        else:
            flash('Only CSV files are allowed')
            return redirect(request.url) #refreshs the page

    return render_template('auto/index.html')

@auto_bp.route('/auto_predict', methods=["POST"])
def auto_predict():
    return render_template('auto/predict.html')