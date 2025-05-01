from flask import Blueprint, render_template, request


# Create the Blueprint object
main_bp = Blueprint('main', __name__, template_folder='templates')

new_patients = []

# Define the routes on the blueprint
@main_bp.route('/', methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        patient = {
            'blood ': request.form['age'],
            'gender': request.form['gender']
        }
        new_patients.append(patient)
    return render_template('index.html')