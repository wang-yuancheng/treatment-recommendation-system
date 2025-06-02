import pandas as pd
import numpy as np
from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from werkzeug.utils import secure_filename
import os, uuid
from app.models import auto_pipeline
from app.paths import *
from app.model.auto_models.auto_model_train import load_dataset
from app.utils import get_csv_path
from app.tasks.train_tasks import train_pipeline_task
from app.celery_app import celery_app
from celery.result import AsyncResult
from app.renamemap import rename_map

# Create the Blueprint object
auto_bp = Blueprint('auto', __name__)

ALLOWED_EXTENSIONS = {'csv'}

# allowed_file(filename) returns True only if the filename contains a dot and the substring
# after the last dot (lowercased) is in the ALLOWED_EXTENSIONS whitelist
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the routes on the blueprint
@auto_bp.route('/auto', methods=["GET"])
def auto_home():
    return render_template('auto/index.html')

@auto_bp.route('/auto/upload', methods=["POST"])
def auto_upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file uploaded')
        return redirect(url_for('auto.auto_home'))

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '' or not allowed_file(file.filename):
        flash('Please select a valid CSV file', 'error')
        return redirect(url_for('auto.auto_home'))

    filename = secure_filename(file.filename)             # Clean the filename to prevent unsafe characters or path traversal
    job_id = str(uuid.uuid4())                            # Create random UUID for each upload
    job_dir = os.path.join(UPLOAD_FOLDER_PATH, job_id)    # Create unique directory for each csv
    os.makedirs(job_dir, exist_ok=True)                   # Creates Upload_Folder, if already exist, continue with no error
    save_path = os.path.join(job_dir, filename)           # Build the full path where the file will be saved
    file.save(save_path)                                  # Save the uploaded file
    flash(f'File saved to {save_path}')

    # redirect to preview page
    return redirect(url_for('auto.auto_preview', job_id=job_id))

@auto_bp.route('/auto/<job_id>', methods=["GET", "POST"])
def auto_preview(job_id):
    # locate the CSV inside the job folder
    csv_path = get_csv_path(job_id)

    # Load Dataframe
    try:
        df = load_dataset(csv_path)
        flash(f"Dataset loaded: {df.shape[0]} rows × {df.shape[1]} cols")
    except Exception as e:
        flash(f"Error loading dataset: {e}", "error")

    # user input for target feature
    if request.method == "POST":
        target = request.form.get("target") # takes in value="{{ col }} and assign it to target
        return redirect(url_for('auto.auto_train', job_id=job_id, target=str(target)))

    # to render the dataframe as a table in html
    return render_template('auto/preview.html',
                           job_id=job_id,
                           column=df.columns,
                           tables=[df.head().to_html(classes='data', index=False)])

@auto_bp.route('/auto/<job_id>/<target>/train', methods=['GET', 'POST'])
def auto_train(job_id, target):
    # Runs the task asynchronously in background, returns a AsyncResult object
    task = train_pipeline_task.delay(job_id, target)

    # Every Celery task is given a unique ID when it's queued. result.id gives you that task ID (string)
    return render_template('auto/loading.html', job_id=job_id, target=target, task_id=task.id) # Get the unique ID of the background task to track its status later

@auto_bp.route('/auto/status/<task_id>', methods=['GET']) # Just reading task status (GET)
def task_status(task_id):
    res = AsyncResult(task_id, app=celery_app)
    response = {'state': res.state,
                'ready': res.state == 'SUCCESS'}
    return jsonify(response)

@auto_bp.route('/auto/<job_id>/<target>/<task_id>/predict', methods=["GET", "POST"])
def auto_predict(job_id, target, task_id):
    res = AsyncResult(task_id, app=celery_app)
    result = res.get() # {'path': path, 'selected_features': selected_features}
    renamed_target = rename_map.get(target, target)  # If target is a key in rename_map, then get returns rename_map[target]
    selected_features = result['selected_features']

    return render_template('auto/predict.html',
                           target=renamed_target,
                           features=selected_features,
                           job_id = job_id,
    )

@auto_bp.route('/auto/result', methods=["POST"])
def auto_result():
    job_id = request.form['job_id']
    selected_features = request.form.getlist('features')

    variables = [
                ('age_years', float), ('gender', int),
                ('height_m', float), ('weight_kg', float),
                ('systolic_bp', float), ('diastolic_bp', float),
                ('cholesterol_level', int), ('glucose_level', int),
                ('smoking_status', int), ('alcohol_consumption', int),
                ('physical_activity', int), ('cardiovascular_disease', int),
        ]

    data = {}

    for name, caster in variables:
            raw = request.form.get(name)  # string or None
            data[name] = caster(raw) if raw else None

    if all(data[k] is not None for k in ('weight_kg', 'height_m')):
            data['body_mass_index'] = data['weight_kg'] / (data['height_m'] ** 2)


    if all(data[k] is not None for k in ('systolic_bp', 'diastolic_bp')):
            data['mean_arterial_pressure'] = (data['systolic_bp'] + 2 * data['diastolic_bp']) / 3
            data['pulse_pressure'] = data['systolic_bp'] - data['diastolic_bp']

    # Build a new dict containing only the keys in selected_features:
    feature_dict = {feat: data.get(feat, np.nan) for feat in selected_features}

    # Then wrap that into a single-row DataFrame:
    df_user = pd.DataFrame([feature_dict])

    pipeline = auto_pipeline(job_id)
    if hasattr(pipeline, "predict_proba"):
        result = pipeline.predict_proba(df_user)[0, 1]  # probability
    else:
        result = pipeline.predict(df_user)[0]  # numeric prediction
        print(f"Prediction: {result}")

    return render_template('auto/result.html', result=result)