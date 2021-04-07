from flask import Blueprint, render_template, redirect, url_for, session, request

from google.cloud import datastore
import os

#Blueprints are use to organize the different pages on a web app.
#The blueprint is connected in the setup of the init.py file

views = Blueprint('views', __name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'website\static\secret\mc-scheduleMaker-ee3731698260.json'
client = datastore.Client()

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        key = client.key('UserCourses', session['userid'])
        entity = datastore.Entity(key=key)
        entity.update({
            'MyClassList': request.form["mylistdata"]
        })
        client.put(entity)
        print(request.form["mylistdata"])
        return redirect(url_for('views.home'))
    else:
        print(session)
        if 'authenticated' in session and session['authenticated']:
            query = client.query(kind="Courses")
            results = list(query.fetch())
            query = client.query(kind="UserCourses") #DOESNT WORK GRABS ALL USERS
            my_key = client.key("UserCourses", session['userid'])
            query.key_filter(my_key, '=')
            userlist = list(query.fetch())
            dictResults = eval(userlist[0]['MyClassList'])
            print(dictResults)
            return render_template('index.html', userid=session['userid'], name=session['name'], image=session['image'], courses=results, mylist=dictResults)
        else:
            return redirect(url_for('auth.login')) #ERROR or SIGN IN FIRST


@views.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        key = client.key('Users', session['userid'])
        entity = datastore.Entity(key=key)
        entity.update({
            'firstname': request.form["first_name"],
            'lastname': request.form["last_name"],
            'campusID': request.form["campusID"],
            'status': str(request.form.get("status")),
            'programOfStudy1': request.form.get("poStudy1"),
            'programOfStudy2': request.form.get("poStudy2"),
            'programOfStudy3': request.form.get("poStudy3"),
            'programOfStudy4': request.form.get("poStudy4"),
            'programOfStudy5': request.form.get("poStudy5"),
            'programOfStudy6': request.form.get("poStudy6"),
            'major1': request.form["major1"],
            'major2': request.form["major2"],
            'minor1': request.form["minor1"],
            'minor2': request.form["minor2"],
            'semester': str(request.form.get("semester")),
            'year': str(request.form.get("year")),
            'advisorEmail': str(request.form.get("advEmail")),
            'gradSem': str(request.form.get("gradSem")),
            'gradYear': str(request.form.get("gradYear")),
            'sign': request.form.get("formCheck-6")
        })
        client.put(entity)
        print(entity)
        return redirect(url_for('views.registration'))
    else:
        print(session)
        if 'authenticated' in session and session['authenticated']:
            return render_template('table.html', userid=session['userid'], name=session['name'], image=session['image'])
        else:
            return redirect(url_for('auth.login')) #ERROR or SIGN IN FIRST
