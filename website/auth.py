from flask import Blueprint, render_template, request, url_for, redirect, session, flash
import json
from oauth2client import client
from google.cloud import datastore
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'website\static\secret\mc-scheduleMaker-ee3731698260.json'
#Blueprints are use to organize the different pages on a web app.
#The blueprint is connected in the setup of the init.py file

auth = Blueprint('auth', __name__)

#GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
#if 'authenticated' in session and session['authenticated']test:

@auth.route('/login/callback', methods = ['POST'])
def login_callback():
    if 'authenticated' not in session:
        if not request.headers.get('X-Requested-With'):
            flash("Login Error", "error")
            return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}

        content_type = request.headers.get("Content-Type")
        auth_code = request.stream if content_type == "application/octet-stream" else request.get_data()
        CLIENT_SECRET_FILE = 'website/static/secret/MC-OAuthSecret.json'

        # Exchange auth code for access token, refresh token, and ID token
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_FILE,
            ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.compose', 'profile', 'email'],
            auth_code)
        if 'hd' not in credentials.id_token or credentials.id_token['hd'] != 'manhattan.edu':
            flash("Please Login Using your Manhattan College Gmail Account ('@manhattan.edu')", "error")
            return json.dumps({'success': False}), 403, {'ContentType': 'application/json'} #NOT MANHATTAN COLLEGE GMAIL
        print('manhattan email passed')
        print(credentials.id_token)
        session['credentials'] = {
            'access_token': credentials.access_token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret
        }
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
        flash("Login Successful", "success")
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': True}), 269, {'ContentType': 'application/json'}


@auth.route('/logout') #Page Route -- A prefix if any is listed in the init.py file
def logout():
    session.clear()
    flash("Logout Successful", "success")
    return redirect(url_for('views.home'))


