from flask import Flask

#INIT FILE - is called main.py and is the setup for the creation of the web app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'MCS_secret'
    #app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app