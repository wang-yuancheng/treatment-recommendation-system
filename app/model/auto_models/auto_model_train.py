import pandas as pd
import os
import joblib

from app.paths import AUTO_MODELS_FOLDER_PATH
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, GridSearchCV

def load_dataset(save_path):
    return pd.read_csv(save_path)

def clean_and_encode_dataset(df, target):
    rename_map = {
        'age (in years)': 'age_years',
        'height (in m)': 'height_m',
        'weight (in kg)': 'weight_kg',
        'bmi (body mass index)': 'body_mass_index',
        'ap_hi (systolic blood pressure)': 'systolic_bp',
        'ap_lo (diastolic blood pressure)': 'diastolic_bp',
        'map (mean arterial pressure)': 'mean_arterial_pressure',
        'pp (pulse pressure)': 'pulse_pressure',
        'cholesterol (1- normal, 2 - above normal, 3- well above normal)': 'cholesterol_level',
        'gluc (1- normal, 2 - above normal, 3- well above normal)': 'glucose_level',
        'gender( 1 for Women, 2 for Men)': 'gender',
        'smoke (0 - does not smoke, 1 - smokes)': 'smoking_status',
        'alco (0 - does not alcohol, 1 - consumes alcohol)': 'alcohol_consumption',
        'active (0 - does not exercise, 1 - exercises)': 'physical_activity',
        'cardio (0 - no cardiovascular disease, 1 -has cardiovascular disease)': 'cardiovascular_disease'
    }
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

    # Remove target from column list
    cont_cols = [col for col in cont_cols if col != target]
    ord_cols = [col for col in ord_cols if col != target]

    # encode features
    scaler = MinMaxScaler()
    # encoded_cont is now a 2D NumPy array of shape (n_rows, len(cont_cols)), where each column has been rescaled.
    encoded_cont = scaler.fit_transform(healthDataRemovedOutliers[cont_cols])
    encoded_cont_cols = pd.DataFrame(encoded_cont, columns=cont_cols, index=healthDataRemovedOutliers.index)

    encoder = OneHotEncoder(drop="first", sparse=False)
    encoded_ord_array = encoder.fit_transform(healthDataRemovedOutliers[ord_cols])
    # The encoder creates N columns, so we pull out the new column names
    new_ord_columns = encoder.get_feature_names_out(ord_cols)
    encoded_ord_cols = pd.DataFrame(encoded_ord_array, columns=new_ord_columns, index=healthDataRemovedOutliers.index)

    encoded_df = pd.concat([encoded_cont_cols, encoded_ord_cols, healthDataRemovedOutliers[target]], axis=1)

    return encoded_df, target

def feature_selection(df, target, threshold) -> list:
    """
    Simple correlation‐based feature selection. Compute the absolute Pearson correlation
    between each feature column and the target. Return those whose |corr| > threshold.
    """

    feature_cols = [col for col in df.columns if col != target]

    # Select features correlated to target
    corr_with_target = df[feature_cols].corrwith(df[target]).abs()
    selected_features = corr_with_target[corr_with_target > threshold].index.tolist()
    return selected_features

def hyperparameter_tuning_and_training(df, target, selected_features):
    X_train, X_test, y_train, y_test = train_test_split(df[selected_features], df[target])

    param_grid_test = {
        'hidden_layer_sizes': [(50,), (100,), (50,50), (200,)],
        'activation': ['relu', 'tanh', 'sigmoid'],
        'solver': ['adam'],
        'alpha': [1e-4],
        'learning_rate': ['constant'],
        'max_iter': [200], # to reduce runtime
        'early_stopping': [True] # to reduce runtime
    }

    """
    param_grid = {
        'hidden_layer_sizes': [(50,), (100,), (50,50), (200,)],
        'activation': ['relu', 'tanh', 'sigmoid'],
        'solver': ['adam', 'sgd'],
        'alpha': [1e-3, 1e-4],
        'learning_rate': ['constant', 'adaptive', 'invscaling'],
    }
    """

    mlp = MLPClassifier()
    grid = GridSearchCV(mlp, param_grid_test, cv=5) # 5-fold cross-validation: Train 4-fold, Test 1-fold
    grid.fit(X_train, y_train) # Returns GirdSearchCV object

    """
    GirdSearchCV Object Attributes
    grid.best_params_: Dictionary of the best hyperparameters
    grid.best_score_: Best average CV score
    grid.best_estimator_: The best MLPClassifier model, fully trained
    """

    return grid.best_estimator_

def run_pipeline(csv_path, target, job_id):
    df = load_dataset(csv_path)
    df, target = clean_and_encode_dataset(df, target)
    selected_features = feature_selection(df, target, threshold=0.3)
    best_model = hyperparameter_tuning_and_training(df, target, selected_features)

    auto_pipeline = Pipeline([
        ("classifier", best_model)
    ])
    model_dir = os.path.join(AUTO_MODELS_FOLDER_PATH, job_id)
    os.makedirs(model_dir, exist_ok=True)
    path = os.path.join(model_dir, 'model.pkl')
    joblib.dump(auto_pipeline, path)
    return path