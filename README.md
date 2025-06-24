# Automated Machine Learning Pipeline

This repository contains code and materials for an end-to-end Flask + Celery Machine Learning application<br><br>
Click [here](data/EDA%20and%20Model%20Comparison/README.md#data-science-workflow) to view the **data science workflow**.<br>
Click [here](app/README.md#model-integration-with-flask) to view the **model integration with Flask**.<br>
Click [here](app/README.md#full-scikit-learn-pipeline) to view the **end-to-end ML pipeline**.

## Key Features

| Component           | Functionality                                                  | Impact                                              |
| ------------------- | -------------------------------------------------------------- | --------------------------------------------------- |
| **AutoML pipeline** | Upload CSV → pick target → Celery trains and saves `model.pkl` | Keeps UI fast while training runs in the background |
| **Custom model**    | Pre-trained MLP (`custompipeline.pkl`) loaded once at startup  | Fast predictions with no delay                      |
| **Dynamic form**    | Form fields auto-generated from selected features              | Ensures input matches model’s expectations          |
| **Modular routes**  | Routes split into `base/`, `custom/`, `auto/` blueprints       | Cleaner code and easier to maintain                 |

## Quick Start

```bash
# 1 Clone & install Python dependencies
git clone https://github.com/wang-yuancheng/AutoMLPipeline.git
cd AutoMLPipeline
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2 Start infrastructure
brew services start rabbitmq
brew services start redis

# 3 Start a Celery worker
celery -A app.celery_app worker --loglevel=info

# 4 Run the Flask dev server
python run.py
```
