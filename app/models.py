import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) # Get root of project

# Build the path to the saved custom_pipeline
# AUTO_PIPELINE_PATH = os.path.join(BASE_DIR, 'model', 'auto_models', 'auto_pipeline.pkl')
CUSTOM_PIPELINE_PATH = os.path.join(BASE_DIR, 'model', 'custom_models', 'custompipeline.pkl')

# Load the pipeline at import time so it's ready for all routes
custom_pipeline = joblib.load(CUSTOM_PIPELINE_PATH)

'''
try:
    auto_pipeline = joblib.load(AUTO_PIPELINE_PATH)
except FileNotFoundError:
    raise RuntimeError(f"Pipeline file not found at {AUTO_PIPELINE_PATH}")
except Exception as e:
    raise RuntimeError(f"Error loading pipeline: {e}")
'''

# for use due to  app.models import *
__all__ = ['custom_pipeline']
# __all__ = ['auto_pipeline', 'custom_pipeline']

