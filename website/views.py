from flask import Blueprint, render_template, redirect, url_for, session, request
import json
from google.cloud import datastore
import os
import website.pdf as pdf
import threading
import time
import website.signature_pdf as spdf

#Blueprints are use to organize the different pages on a web app.
#The blueprint is connected in the setup of the init.py file


views = Blueprint('views', __name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'website\static\secret\mc-scheduleMaker-ee3731698260.json'
client = datastore.Client()
client2 = datastore.Client()

@views.route('/', methods=['GET', 'POST'])
def home():
    if 'authenticated' in session and session['authenticated']:
        if request.method == 'POST':
            key = client.key('UserCourses', session['userid'])
            entity = datastore.Entity(key=key)
            entity.update({
                'MyClassList': request.form["mylistdata"]
            })
            client.put(entity)
            print(request.form["mylistdata"])
            return redirect(url_for('views.home')) #CHANGE TO return '', 204 after fixing visual bug
        else:
            print(session)
            if 'authenticated' in session and session['authenticated']:
                query = client.query(kind="Courses")
                results = list(query.fetch())
                query = client.query(kind="UserCourses")  # DOESNT WORK GRABS ALL USERS
                my_key = client.key("UserCourses", session['userid'])
                query.key_filter(my_key, '=')
                userlist = list(query.fetch())
                try:
                    dictResults = eval(userlist[0]['MyClassList'])
                    print(dictResults)
                except IndexError:
                    dictResults = {}
                return render_template('login_index.html', userid=session['userid'], name=session['name'],
                                       image=session['image'], courses=results, mylist=dictResults)
            else:
                return redirect(url_for('auth.login'))  # ERROR or SIGN IN FIRST
    else:
        if request.method == 'POST': #DELETE POST FOR THIS PART ((CHECK THIS))
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
    elif (list(newjs_on)[0]) == 'update':
        data = newjs_on[(list(newjs_on)[0])]
        (session['mylist'])[(data[0])][2] = data[1]
        session.modified = True
    else:
        data = newjs_on['remove']
        if session['mylist'][data.strip()] is not None:
            del session['mylist'][data.strip()]
            session.modified = True
    return '', 204

@views.route('/spam', methods=['POST'])
def spam():
    return '', 204

@views.route('/registration', methods=['GET', 'POST'])
def registration():

    if 'authenticated' in session and session['authenticated']:
        if request.method == 'POST':
            key = client.key('Users', session['userid'])
            entity = datastore.Entity(key=key)
            entity.update({
                'data': [
                    request.form["first_name"],
                    request.form["last_name"],
                    request.form["campusID"],
                    str(request.form.get("status")),
                    request.form.get("poStudy1"),
                    request.form.get("poStudy2"),
                    request.form.get("poStudy3"),
                    request.form.get("poStudy4"),
                    request.form.get("poStudy5"),
                    request.form.get("poStudy6"),
                    request.form["major1"],
                    request.form["major2"],
                    request.form["minor1"],
                    request.form["minor2"],
                    str(request.form.get("semester")),
                    str(request.form.get("year")),
                    str(request.form.get("advEmail")),
                    str(request.form.get("gradSem")),
                    str(request.form.get("gradYear")),
                    request.form.get("formCheck-6")
                ]
            })
            client.put(entity)
            print(entity)
            return redirect(url_for('views.registration'))
        else:
            query = client.query(kind="UserCourses")
            my_key = client.key("UserCourses", session['userid'])
            query.key_filter(my_key, '=')
            userlist = list(query.fetch())
            query_user = client2.query(kind="Users")
            key = client2.key('Users', session['userid'])
            query_user.key_filter(key, '=')
            userdata = list(query_user.fetch())
            print('here')
            print(userdata)
            try:
                dictResults = eval(userlist[0]['MyClassList'])
                print(dictResults)
            except IndexError:
                dictResults = {}
            try:
                p_data = userdata[0]['data']
                print(p_data)
            except (IndexError, KeyError) as keyindex:
                p_data = []
            if dictResults == {}:
                cred = 0
                courses = 0
                path = "./static/pdf/undergraduate_registration_form_latest.pdf?v=" + str(time.time())
            else:
                name, cred, courses = pdf.runfull(dictResults, p_data)
                name = name.split('/')[-1]
                path = './static/pdf/' + name
                delpath = 'website/static/pdf/' + name
                if p_data != [] and p_data[19] is not None:
                    fullp_name = p_data[0]+' '+p_data[1]
                    spdf.run(fullp_name, delpath)
                del_thread = threading.Thread(target=delay_delete, args=(5, delpath))
                del_thread.start()
            return render_template('login_table.html', userid=session['userid'], name=session['name'], image=session['image'], cred=cred, courses=courses, path=path, p_data=p_data)
    else:
        try:
            dictResults = session['mylist']
            print(dictResults)
        except KeyError:
            dictResults = {}
        if dictResults == {}:
            cred = 0
            courses = 0
            path = "./static/pdf/undergraduate_registration_form_latest.pdf?v=" + str(time.time())
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