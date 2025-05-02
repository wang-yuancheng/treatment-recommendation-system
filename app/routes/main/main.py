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
        data = request.form.get('csv_input')

        #convert csv into expected input
        age, bmi, sbp, dbp, chol_cat, gluc_cat = data.split(',')
        age = float(age)
        bmi = float(bmi)
        sbp = float(sbp)
        dbp = float(dbp)
        chol_cat = int(chol_cat)
        gluc_cat = int(gluc_cat)

        df_user = pd.DataFrame([{
            'age_years': age,
            'body_mass_index': bmi,
            'systolic_bp': sbp,
            'diastolic_bp': dbp,
            'cholesterol_level': chol_cat,
            'glucose_level': gluc_cat
        }])

        proba = pipeline.predict_proba(df_user)[0, 1]  # returns class 1: probability of disease
        print(f"Predicted cardiovascular risk: {proba:.3f}")

        return render_template('predict.html', result=proba)