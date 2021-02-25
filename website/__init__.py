from flask import Flask
import os
#INIT FILE - is called main.py and is the setup for the creation of the web app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_FLASK", None)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app