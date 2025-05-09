import os

ROOT = os.path.dirname(os.path.dirname(__file__)) # Get root of project, two dirname calls

# Build the path to the saved custom_pipeline
AUTO_MODELS_FOLDER_PATH = os.path.join(ROOT,'app', 'model', 'auto_models')
CUSTOM_PIPELINE_PATH = os.path.join(ROOT, 'app', 'model', 'custom_models', 'custompipeline.pkl')
UPLOAD_FOLDER_PATH = os.path.join(ROOT, 'app', 'Upload_Folder')

# for app.paths import *
__all__ = ['ROOT', 'AUTO_MODELS_FOLDER_PATH', 'CUSTOM_PIPELINE_PATH', 'UPLOAD_FOLDER_PATH']
