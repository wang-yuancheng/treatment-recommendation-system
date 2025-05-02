import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import joblib

healthDataRaw = pd.read_csv('../data/cardio_train.csv')

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
healthData = healthDataRaw.rename(columns=rename_map)

healthDataClean = healthData.copy()

# removing entries with values less than 0 for blood pressure, pulse pressure and arterial pressure (medically impossible values)
healthDataClean = healthDataClean[
                        (healthDataClean['systolic_bp'] > 0) &
                        (healthDataClean['diastolic_bp'] > 0) &
                        (healthDataClean['pulse_pressure'] > 0) &
                        (healthDataClean['mean_arterial_pressure'] > 0)
]

# reset index of dataframe as we removed some rows
healthDataClean = healthDataClean.reset_index(drop=True)

# define variable types
continuous_cols = ['age_years', 'height_m', 'weight_kg', 'body_mass_index', 'systolic_bp', 'diastolic_bp', 'mean_arterial_pressure', 'pulse_pressure']
binary_cols = ['smoking_status', 'alcohol_consumption', 'physical_activity', 'gender']
ordinal_cols = ['cholesterol_level', 'glucose_level']

healthDataRemovedOutliers = healthDataClean.copy() #just in case we need healthDataClean dataframe

# remove outliers for continuous variables
for col in continuous_cols:
    Q1 = healthDataClean[col].quantile(0.25)
    Q3 = healthDataClean[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    healthDataRemovedOutliers = healthDataRemovedOutliers[healthDataRemovedOutliers[col].between(lower, upper)]

# split into features(X) and target(y)
X_df = healthDataRemovedOutliers[continuous_cols + binary_cols + ordinal_cols]
y = healthDataRemovedOutliers['cardiovascular_disease']

# build the transformer: MinMaxScale continuous and binary variables, OneHotEncode ordinal columns
preprocessor = ColumnTransformer(transformers=[
    ('scale', MinMaxScaler(), continuous_cols + binary_cols),
    ('ohe',   OneHotEncoder(drop='first', sparse_output=False), ordinal_cols), #drop='first' to avoid collinearity and remove redundancy, sparse=False makes the output a regular array
])
X_array = preprocessor.fit_transform(X_df)

# turn X_array back into a DataFrame with original names
ohe_names = preprocessor.named_transformers_['ohe'].get_feature_names_out(ordinal_cols)
all_feature_names = continuous_cols + binary_cols + list(ohe_names)
df_encoded_features = pd.DataFrame(X_array, columns=all_feature_names, index=healthDataRemovedOutliers.index)

# Now df_encoded_features is the feature matrix and y is the target vector