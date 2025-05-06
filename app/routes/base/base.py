from flask import Blueprint, render_template, request
from app.models import *
import pandas as pd

# Create the Blueprint object
base_bp = Blueprint('base', __name__, template_folder='templates')

# Define the routes on the blueprint
@base_bp.route('/', methods=["GET"])
def home():
    return render_template('base.html')
