from flask import Blueprint, render_template, redirect, url_for, session

from google.cloud import datastore
import os

#Blueprints are use to organize the different pages on a web app.
#The blueprint is connected in the setup of the init.py file

views = Blueprint('views', __name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'website\static\secret\mc-scheduleMaker-ee3731698260.json'
client = datastore.Client()

@views.route('/')
def home():
    print(session)
    if 'authenticated' in session and session['authenticated']:
        query = client.query(kind="Courses")
        results = list(query.fetch())
        return render_template('index.html', userid=session['userid'], name=session['name'], image=session['image'], courses=results)
    else:
        return redirect(url_for('auth.login')) #ERROR or SIGN IN FIRST - TEST

@views.route('/registration')
def registration():
    print(session)
    if 'authenticated' in session and session['authenticated']:
        return render_template('table.html', userid=session['userid'], name=session['name'], image=session['image'])
    else:
        return redirect(url_for('auth.login')) #ERROR or SIGN IN FIRST