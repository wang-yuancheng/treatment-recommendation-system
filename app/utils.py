import glob, os
from app.paths import *

def get_csv_path(job_id):
    job_dir = os.path.join(UPLOAD_FOLDER_PATH, job_id)
    matches = glob.glob(os.path.join(str(job_dir), '*.csv'))
    if not matches:
        raise FileNotFoundError(f"No CSV found for job {job_id!r}")
    return matches[0]