from flask import Blueprint, render_template, request, url_for, redirect, session
import json
from oauth2client import client
from google.cloud import datastore
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'website\static\secret\MCS-Capstone-94761bef3d8d.json'
#Blueprints are use to organize the different pages on a web app.
#The blueprint is connected in the setup of the init.py file

auth = Blueprint('auth', __name__)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

@auth.route('/login') #Page Route -- A prefix if any is listed in the init.py file
def login():
    if 'authenticated' in session and session['authenticated']:
        return redirect(url_for('views.home'))
    else:
        return render_template('login.html')

@auth.route('/login/callback', methods = ['POST'])
def login_callback():
    if not request.headers.get('X-Requested-With'):
        return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}

    content_type = request.headers.get("Content-Type")
    auth_code = request.stream if content_type == "application/octet-stream" else request.get_data()
    CLIENT_SECRET_FILE = 'website/static/secret/client_secret_205736862006-gun9p9davgcd32tj50ldlsg8u0ej8mjg.apps.googleusercontent.com.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['profile', 'email'],
        session['auth_code'])
    print(credentials.id_token)
    if 'hd' not in credentials.id_token or credentials.id_token['hd'] != 'manhattan.edu':
        return json.dumps({'success': False}), 403, {'ContentType': 'application/json'} #NOT MANHATTAN COLLEGE GMAIL

    client_2 = datastore.Client()
    key = client_2.key('Users', credentials.id_token['sub'])
    result = client_2.get(key)
    if result is None:
        entity = datastore.Entity(key=key)
        entity.update({
            'AdvisorID': 'None'
        })
        client_2.put(entity)

    # Get profile info from ID token
    session['authenticated'] = True
    session['userid'] = credentials.id_token['sub']
    session['name'] = credentials.id_token['name']
    session['image'] = credentials.id_token['picture']
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@auth.route('/logout') #Page Route -- A prefix if any is listed in the init.py file
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


