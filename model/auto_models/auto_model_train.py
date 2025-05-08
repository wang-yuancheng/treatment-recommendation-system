import pandas as pd
import os
import joblib
from app.paths import AUTO_MODELS_FOLDER_PATH
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.neural_network import MLPClassifier

def load_dataset(save_path):
    df = pd.read_csv(save_path)
    return df

def remove_outliers():
    pass

def feature_selection():
    pass

def train_model():
    pass

def hyperparameter_tuning():
    pass

def run_pipeline(df, features, target, job_id):
    '''
    # save model for deployment
    model_dir = os.path.join(AUTO_MODELS_FOLDER_PATH, job_id)
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(str(model_dir), "custompipeline.pkl")
    joblib.dump(fitted_pipeline, model_path)
    '''
    pass