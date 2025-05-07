import joblib
from app.paths import *

# Load the pipeline at import time so it's ready for all routes
# auto_pipeline = joblib.load(AUTO_PIPELINE_PATH)
custom_pipeline = joblib.load(CUSTOM_PIPELINE_PATH)

# for app.models import *
__all__ = ['custom_pipeline']
# __all__ = ['auto_pipeline', 'custom_pipeline']

