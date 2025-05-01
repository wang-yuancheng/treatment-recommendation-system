from flask import Flask
from app.routes.main import main_bp

def create_app(): #creates an application and returns it as an object so that it is not always executed when you import the application file
    app = Flask(__name__, template_folder='templates') #new flask application is created with a specified template folder

    #register the blueprint
    app.register_blueprint(main_bp)

    return app