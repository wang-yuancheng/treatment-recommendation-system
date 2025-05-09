import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.neural_network import MLPClassifier

healthDataRaw = pd.read_csv('../../../../data/cardio_train.csv')

# assuming your DataFrame is named df_clean
rename_map = {
    'age (in years)':                                                        'age_years',
    'height (in m)':                                                         'height_m',
    'weight (in kg)':                                                        'weight_kg',
    'bmi (body mass index)':                                                 'body_mass_index',
    'ap_hi (systolic blood pressure)':                                       'systolic_bp',
    'ap_lo (diastolic blood pressure)':                                      'diastolic_bp',
    'map (mean arterial pressure)':                                          'mean_arterial_pressure',
    'pp (pulse pressure)':                                                   'pulse_pressure',
    'cholesterol (1- normal, 2 - above normal, 3- well above normal)':       'cholesterol_level',
    'gluc (1- normal, 2 - above normal, 3- well above normal)':              'glucose_level',
    'gender( 1 for Women, 2 for Men)':                                       'gender',
    'smoke (0 - does not smoke, 1 - smokes)':                                'smoking_status',
    'alco (0 - does not alcohol, 1 - consumes alcohol)':                     'alcohol_consumption',
    'active (0 - does not exercise, 1 - exercises)':                         'physical_activity',
    'cardio (0 - no cardiovascular disease, 1 -has cardiovascular disease)': 'cardiovascular_disease'
}
healthDataRenamed = healthDataRaw.rename(columns=rename_map)

# removing entries with values less than 0 for blood pressure, pulse pressure and arterial pressure (medically impossible values)
healthDataValid = healthDataRenamed[
                        (healthDataRenamed['systolic_bp'] > 0) &
                        (healthDataRenamed['diastolic_bp'] > 0) &
                        (healthDataRenamed['pulse_pressure'] > 0) &
                        (healthDataRenamed['mean_arterial_pressure'] > 0)
].reset_index(drop=True) # reset index of dataframe as we removed some rows

# remove outliers for continuous features
continuous_cols = ['age_years', 'height_m', 'weight_kg', 'body_mass_index', 'systolic_bp', 'diastolic_bp', 'mean_arterial_pressure', 'pulse_pressure']
for col in continuous_cols:
    Q1 = healthDataValid[col].quantile(0.25)
    Q3 = healthDataValid[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    healthDataValid = healthDataValid[healthDataValid[col].between(lower, upper)]
healthDataRemovedOutliers = healthDataValid.reset_index(drop=True)

# select age, bmi, sys_bp, dia_bp, cholesterol_level, glucose_level after dimensionality reduction and feature selection
selected_cont_features = ['age_years', 'body_mass_index', 'systolic_bp', 'diastolic_bp',]
selected_ord_features = ['cholesterol_level', 'glucose_level']

# split into features(X) and target(y)
# no need to train test split here as we want to train the model on the whole dataset to improve model performance in deployment
X_df = healthDataRemovedOutliers[selected_cont_features + selected_ord_features]
y = healthDataRemovedOutliers['cardiovascular_disease']

# build the preprocessor that encodes cont features using MinMaxScaling and ordinary features with one-hot encoding
preprocessor = ColumnTransformer([
    ('scale', MinMaxScaler(), selected_cont_features),
    ('ohe', OneHotEncoder(drop='first', sparse_output=False), selected_ord_features),
])

# combine preprocessor with chosen model: Multi-Layer-Perceptron
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', MLPClassifier(hidden_layer_sizes=(100, ), max_iter=200)),
])

# fit the pipeline
pipeline.fit(X_df, y)

# save model for deployment
joblib.dump(pipeline, 'custompipeline.pkl')