from flask import Flask
from app.routes.custom import custom_bp

def create_app(): #creates an application and returns it as an object so that it is not always executed when you import the application file
    app = Flask(__name__, static_folder='static', static_url_path='/static', template_folder='templates')
    # app = Flask(__name__) implicitly:
    # static_folder='static'
    # static_url_path='/static'
    # template_folder='templates'

    #register the blueprint
    app.register_blueprint(custom_bp)

    return app