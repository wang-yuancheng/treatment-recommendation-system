# @celery.task functions live here
# turn your training function into a Celery task
# then launch a worker to pick up those tasks.
from pyexpat import features

from app.celery_app import celery_app
from app.utils import get_csv_path
from app.model.auto_models.auto_model_train import run_pipeline

# This is a Celery background task for training an ML pipeline.
# It loads the dataset for a given job_id, selects features, trains the model,
# saves it to disk, and returns the path to the saved model.
@celery_app.task(bind=True)
def train_pipeline_task(self, job_id, target): # define a task function, self: refers to the task instance (only available because of bind=True)
    csv_path = get_csv_path(job_id)
    # Train the model and save it; run_pipeline returns the saved model path
    path = run_pipeline(csv_path, target, job_id) # only assigns return value: .pkl path only when run_pipeline is done
    return path