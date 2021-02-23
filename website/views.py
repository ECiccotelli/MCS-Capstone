from flask import Blueprint, render_template, redirect, url_for, session
#Blueprints are use to organize the different pages on a web app.
#The blueprint is connected in the setup of the init.py file

views = Blueprint('views', __name__)

@views.route('/')
def home():
    print(session)
    if 'authenticated' in session and session['authenticated']:
        return render_template('index.html', userid=session['userid'], name=session['name'], image=session['image'])
    else:
        redirect(url_for('auth.login')) #ERROR or SIGN IN FIRST

