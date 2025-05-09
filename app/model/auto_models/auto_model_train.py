import pandas as pd
import os
import joblib
from app.paths import AUTO_MODELS_FOLDER_PATH
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.neural_network import MLPClassifier

def load_dataset(save_path):
    return pd.read_csv(save_path)

def remove_outliers():
    pass

def feature_selection():
    pass

def train_model():
    pass

def hyperparameter_tuning():
    pass

def run_pipeline(df, features, target, job_id):
    """
    1) Builds X/y from df, features, target
    2) Trains & tunes the model
    3) Packages everything into a sklearn Pipeline
    4) Dumps the pipeline to disk under AUTO_MODELS_FOLDER_PATH/job_id/custompipeline.pkl
    5) Returns the fitted Pipeline object
    """

    # 1) Extract X, y
    # 2) Clean
    # 3) Train
    # 4) Wrap in a Pipeline (e.g. with preprocessors)
    '''
    pipe = Pipeline([
      ('pre', ColumnTransformer([
         ('scale', MinMaxScaler(), features),
         ('ohe',   OneHotEncoder(drop='first', sparse_output=False), [])
      ])),
      ('clf', best_model)
    ])

    pipe.fit(X, y)
    '''

    # 5) Dump it
    '''
    model_dir = os.path.join(AUTO_MODELS_FOLDER_PATH, job_id)
    os.makedirs(model_dir, exist_ok=True)
    path = os.path.join(model_dir, 'custompipeline.pkl')
    joblib.dump(pipe, path)
    '''
    pass