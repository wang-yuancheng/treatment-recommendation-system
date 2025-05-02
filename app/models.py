import os
import joblib

# Build the path to the saved pipeline
BASE_DIR      = os.path.dirname(os.path.dirname(__file__)) # Get root of project (treatment-recommendation-system)
PIPELINE_PATH = os.path.join(BASE_DIR, 'model', 'pipeline.pkl')

# Load the pipeline at import time so it's ready for all routes
pipeline = joblib.load(PIPELINE_PATH)

# Expose only 'pipeline' for cleaner imports
__all__ = ['pipeline']
