from flask import Blueprint, render_template, request
from app.models import *
import pandas as pd

# Create the Blueprint object
auto_bp = Blueprint('custom', __name__, template_folder='templates')

# Define the routes on the blueprint
@auto_bp.route('/auto', methods=["GET"])
def home():
    return render_template('index.html')

@auto_bp.route('/auto_predict', methods=["POST"])
def predict():
    return render_template('predict.html', result=proba)