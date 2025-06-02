import pandas as pd
import os
import joblib

from app.paths import AUTO_MODELS_FOLDER_PATH
from app.renamemap import rename_map
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.utils.multiclass import type_of_target

def load_dataset(save_path):
    return pd.read_csv(save_path)

def clean_dataset(df, target):
    healthDataRenamed = df.rename(columns=rename_map)

    if target in rename_map:
        target = rename_map[target]
    elif target in rename_map.values():
        # already the renamed version, so leave it alone
        target = target
    else:
        raise KeyError(f"'{target}' not found in rename_map")

    healthDataValid = healthDataRenamed[
        (healthDataRenamed['systolic_bp'] > 0) &
        (healthDataRenamed['diastolic_bp'] > 0) &
        (healthDataRenamed['pulse_pressure'] > 0) &
        (healthDataRenamed['mean_arterial_pressure'] > 0)
        ].reset_index(drop=True)  # reset index of dataframe as we removed some rows

    # remove outliers for continuous features
    cont_cols = ['age_years', 'height_m', 'weight_kg', 'body_mass_index', 'systolic_bp', 'diastolic_bp',
                 'mean_arterial_pressure', 'pulse_pressure']
    ord_cols = ['cholesterol_level', 'glucose_level', 'gender', 'smoking_status', 'alcohol_consumption',
                'physical_activity', 'cardiovascular_disease']

    # remove outliers
    for col in cont_cols:
        Q1 = healthDataValid[col].quantile(0.25)
        Q3 = healthDataValid[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        healthDataValid = healthDataValid[healthDataValid[col].between(lower, upper)]
    healthDataRemovedOutliers = healthDataValid.reset_index(drop=True)
    return healthDataRemovedOutliers, target

def feature_selection(df, target, threshold) -> list:
    """
    Simple correlation‐based feature selection. Compute the absolute Pearson correlation
    between each feature column and the target. Return those whose |corr| > threshold.
    """

    feature_cols = [col for col in df.columns if col != target]

    # Select features correlated to target
    corr_with_target = df[feature_cols].corrwith(df[target]).abs()
    selected_features = corr_with_target[corr_with_target > threshold].index.tolist()

    # Create 2 lists of cont and ord of selected_features
    selected_features_cont = []
    selected_features_ord = []
    cont_cols = ['age_years', 'height_m', 'weight_kg', 'body_mass_index', 'systolic_bp', 'diastolic_bp',
                 'mean_arterial_pressure', 'pulse_pressure']
    ord_cols = ['cholesterol_level', 'glucose_level', 'gender', 'smoking_status', 'alcohol_consumption',
                'physical_activity', 'cardiovascular_disease']
    for col in selected_features:
        if col in cont_cols:
            selected_features_cont.append(col)
        elif col in ord_cols:
            selected_features_ord.append(col)

    return selected_features, selected_features_cont, selected_features_ord

def hyperparameter_tuning_and_training(X_train, y_train, y_type):
    if y_type == "continuous":
        model       = MLPRegressor(max_iter=200, random_state=42)
        param_grid  = {
            "hidden_layer_sizes": [(50,), (100,), (50, 50)],
            "activation": ["relu", "tanh", "logistic"],
            "solver": ["adam"],
            "alpha": [1e-4],
            "learning_rate": ["constant"],
            "early_stopping": [True],
        }
    else:
        model       = MLPClassifier(max_iter=200, random_state=42)
        param_grid  = {
            "hidden_layer_sizes": [(50,), (100,), (50, 50)],
            "activation": ["relu", "tanh", "logistic"],
            "solver": ["adam"],
            "alpha": [1e-4],
            "learning_rate": ["constant"],
            "early_stopping": [True],
        }

    grid = GridSearchCV(model, param_grid, cv=5, n_jobs=-1)
    grid.fit(X_train, y_train)
    return grid.best_estimator_

def run_pipeline(csv_path, target, job_id):
    df = load_dataset(csv_path)
    df, target = clean_dataset(df, target) # return healthDataRemovedOutliers, target
    selected_features, selected_features_cont, selected_features_ord = feature_selection(df, target, threshold=0.05)

    X = df[selected_features]
    y = df[target]
    y_type = type_of_target(y)

    model = hyperparameter_tuning_and_training(X, y, y_type)

    transformers = []
    if selected_features_cont:  # only add if list non-empty
        transformers.append(
            ("scale", MinMaxScaler(), selected_features_cont)
        )

    if selected_features_ord:  # only add if list non-empty
        transformers.append(
            ("ohe",
             OneHotEncoder(drop="first",
                           handle_unknown="ignore",
                           sparse_output=False),
             selected_features_ord)
        )

    if not transformers:
        raise ValueError("No features passed the correlation threshold.")

    preprocessor = ColumnTransformer(transformers, remainder="drop")

    auto_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ("classifier", model)
    ])

    auto_pipeline.fit(X, y)

    model_dir = os.path.join(AUTO_MODELS_FOLDER_PATH, job_id)
    os.makedirs(model_dir, exist_ok=True)
    path = os.path.join(str(model_dir), 'model.pkl')
    joblib.dump(auto_pipeline, path)
    return path, selected_features