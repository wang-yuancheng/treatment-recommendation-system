from flask import Blueprint, render_template, request, url_for, redirect

# Create the Blueprint object
base_bp = Blueprint('base', __name__)

# Define the routes on the blueprint
@base_bp.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        userinput = request.form.get("ml")
        if userinput == "auto":
            return redirect(url_for('auto.auto_home')) # url_for(blueprint_name.function_name)
        if userinput == "custom":
            return redirect(url_for('custom.cardio_home')) # Flask looks up 'cardio.home' in its internal URL map which was has blueprint already registered
    return render_template('base/base.html')