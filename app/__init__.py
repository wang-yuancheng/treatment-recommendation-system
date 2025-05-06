from flask import Flask
from app.routes.base import base_bp
from app.routes.custom import custom_bp
from app.routes.auto import auto_bp
import os

def create_app(): #creates an application and returns it as an object so that it is not always executed when you import the application file
    app = Flask(__name__) # implicitly sets static_folder='static' static_url_path='/static' template_folder='templates'

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # app.config is a normal Python dictionary that lives on your Flask(__name__) object.
    # assign filesystem path to app.config['UPLOAD_FOLDER']
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Upload_Folder')

    #register the blueprints
    app.register_blueprint(base_bp)
    app.register_blueprint(custom_bp)
    app.register_blueprint(auto_bp)

    return app