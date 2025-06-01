# brew install redis
# brew install rabbitmq
# brew services start redis
# brew services start rabbitmq

from celery import Celery

# Create a Celery app using the current module name (celery_app.py)
def create_celery_app(app_name=__name__):
    return Celery(app_name,                                        # Initialize Celery with the given app name
                  broker='pyamqp://guest:guest@127.0.0.1//',       # RabbitMQ message broker
                  backend='redis://127.0.0.1:6379/1')              # Redis result backend

# The Celery worker will use this app instance when launched via:
# celery -A app.celery_app worker --loglevel=info > basically: from app.celery_app import app

celery_app = create_celery_app() # Initialize Celery app with Redis config
app = celery_app