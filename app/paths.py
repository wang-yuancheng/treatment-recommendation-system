import os

ROOT = os.path.dirname(os.path.dirname(__file__)) # Get root of project, two dirname calls

# Build the path to the saved custom_pipeline
# AUTO_PIPELINE_PATH = os.path.join(ROOT, 'model', 'auto_models', 'auto_pipeline.pkl')
CUSTOM_PIPELINE_PATH = os.path.join(ROOT, 'model', 'custom_models', 'custompipeline.pkl')
UPLOAD_FOLDER_PATH = os.path.join(ROOT, 'app', 'Upload_Folder')

# for app.paths import *
__all__ = ['ROOT', 'CUSTOM_PIPELINE_PATH', 'UPLOAD_FOLDER_PATH']
