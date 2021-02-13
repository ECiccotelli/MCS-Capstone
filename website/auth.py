from flask import Blueprint, render_template
#Blueprints are use to organize the different pages on a web app.
#The blueprint is connected in the setup of the init.py file

auth = Blueprint('auth', __name__)

@auth.route('/login') #Page Route -- A prefix if any is listed in the init.py file
def login():
    return render_template('login.html')

@auth.route('/logout') #Page Route -- A prefix if any is listed in the init.py file
def logout():
    return '<p>Logout Page</>'


