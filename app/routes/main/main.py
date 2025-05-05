from flask import Blueprint, render_template, request
from app.models import pipeline
import pandas as pd

# Create the Blueprint object
main_bp = Blueprint('main', __name__, template_folder='templates')

# Define the routes on the blueprint
@main_bp.route('/', methods=["GET"])
def home():
    return render_template('index.html')

@main_bp.route('/predict', methods=["POST"])
def predict():
    data = {} #create a dictionary to store patient data
    variables = ['age', 'gender', 'height', 'weight', 'sbp', 'dbp', 'chol', 'gluc', 'smoke', 'alcohol', 'active']
    var_types = [float, int, float, float, float, float, int, int, int, int, int]

    #transfer patient data to data dictionary
    for var, var_type in zip(variables, var_types):
        data[var] = request.form.get(var, type=var_type)

    data['bmi'] = data['weight'] / (data['height'] ** 2) # BMI = Weight / Height^2
    data['MAP'] = (data['sbp'] + 2 * data['dbp']) / 3    # Mean Arterial Pressure = (SBP + 2·DBP) / 3
    data['PP'] = data['sbp'] - data['dbp']               # Pulse Pressure = SBP − DBP

    #for now, we only these values are expected by the model
    df_user = pd.DataFrame([{
        'age_years': data["age"],
        'body_mass_index': data["bmi"],
        'systolic_bp': data["sbp"],
        'diastolic_bp': data["dbp"],
        'cholesterol_level': data["chol"],
        'glucose_level': data["gluc"]
    }])

    proba = pipeline.predict_proba(df_user)[0, 1]  # returns class 1: probability of disease
    print(f"Predicted cardiovascular risk: {proba:.3f}")

    return render_template('predict.html', result=proba)