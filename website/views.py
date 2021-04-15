from flask import Blueprint, render_template, redirect, url_for, session, request, after_this_request
import json
from google.cloud import datastore
import os
import website.pdf as pdf
import threading
import time

#Blueprints are use to organize the different pages on a web app.
#The blueprint is connected in the setup of the init.py file

views = Blueprint('views', __name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'website\static\secret\mc-scheduleMaker-ee3731698260.json'
client = datastore.Client()

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.data) #LOGIN
    query = client.query(kind="Courses")
    results = list(query.fetch())
    try:
        dictResults = session['mylist']
        print(dictResults)
    except KeyError:
        dictResults = {}
    return render_template('index.html', courses=results, mylist=dictResults)

@views.route('/h_update', methods=['POST'])
def home_update():
    js_on = (request.get_data().decode("utf-8")).replace("'", "\"")
    newjs_on = json.loads(js_on)
    if 'mylist' not in session:
        session['mylist'] = {}
        #session['mylist'][list(newjs_on)[0]] = request.get_data().decode("utf-8")
    if (list(newjs_on)[0]) == 'append':
        data = newjs_on[(list(newjs_on)[0])]
        (session['mylist'])[(data[0])] = [data[1], data[2], data[3], data[4]]
        session.modified = True
    else:
        data = newjs_on['remove']
        if session['mylist'][data.strip()] is not None:
            del session['mylist'][data.strip()]
            session.modified = True
    return '', 204
'''
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
            try:
                dictResults = eval(userlist[0]['MyClassList'])
                print(dictResults)
            except IndexError:
                dictResults = {}
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
        return render_template('table.html', userid=session['userid'], name=session['name'], image=session['image'])
'''

@views.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        pass
    try:
        dictResults = session['mylist']
        print(dictResults)
    except KeyError:
        dictResults = {}
    if dictResults == {}:
        cred = 0
        courses = 0
        path = "./static/pdf/undergraduate_registration_form.pdf"
    else:
        name, cred, courses = pdf.run(dictResults)
        name = name.split('/')[-1]
        path = './static/pdf/'+name
        delpath = 'website/static/pdf/'+name
        del_thread = threading.Thread(target=delay_delete, args=(5, delpath))
        del_thread.start()
    return render_template('table.html', path=path, cred=cred, courses=courses)

def delay_delete(delay, path):
    print("started")
    time.sleep(delay)
    print("trying to delete")
    os.remove(path)
    print("done")
    return