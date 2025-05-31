import joblib
import os
from app.paths import *

# Load the pipeline at import time so it's ready for all routes
custom_pipeline = joblib.load(CUSTOM_PIPELINE_PATH)

def auto_pipeline(job_id):
    """
    Given a job_id UUID, look in the configured pipeline folder,
    load that job’s pipeline.pkl, and return it.
    """
    job_specific_path = os.path.join(AUTO_MODELS_FOLDER_PATH, job_id, 'model.pkl')
    if not os.path.exists(job_specific_path):
        raise FileNotFoundError(f"No pipeline found for job {job_id!r}")
    return joblib.load(job_specific_path)

# for app.models import *
__all__ = ['auto_pipeline', 'custom_pipeline']