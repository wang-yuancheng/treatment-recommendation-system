# brew install redis
# brew services start redis

from celery import Celery

# Create a Celery app using the current module name
def create_celery_app(app_name=__name__):              # Set default name based on the current module
    return Celery(app_name,                            # Initialize Celery with the given app name
                  broker='redis://127.0.0.1:6379/0',   # Redis used as the message broker: Get tasks (DB 0/16)
                  backend='redis://127.0.0.1:6379/1')  # Redis used to store task results: Store results (DB 1/16)

# Change to 'redis://redis:6379/1' if we have a Docker Compose service called “redis”

# TODO: In production, this Celery app will be run as a separate service using Docker Compose.
# Redis will also be managed as a Docker container. This setup allows Flask (web),
# Celery (worker), and Redis (message broker) to run as independent, scalable services.
# The Celery worker will use this app instance when launched via:
# celery -A app.celery_app worker --loglevel=info

celery_app = create_celery_app() # Initialize Celery app with Redis config

