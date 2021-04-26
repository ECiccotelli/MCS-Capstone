import base64
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, render_template, redirect, url_for, session, request, flash
import json
from google.cloud import datastore
import os

from googleapiclient import errors
import google.oauth2.credentials
import website.pdf as pdf
import threading
import time
import website.signature_pdf as spdf
from googleapiclient.discovery import build

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
            flash("Courses Saved", "save")
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
                return redirect(url_for('views.home'))  # ERROR or SIGN IN FIRST
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

@views.route('/help', methods=['GET'])
def faq_help():
    return render_template('faq_help.html')

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

@views.route('/email', methods=['POST'])
def email():
    js_on = (request.get_data().decode("utf-8")).replace("'", "\"")
    data_json = json.loads(js_on)
    if (list(data_json)[0]) == 'send':
        data = data_json[(list(data_json)[0])]
        fullname_addon = session['name'].replace(" ", "_")
        credentials = google.oauth2.credentials.Credentials(
            session["credentials"]["access_token"],
            refresh_token=session["credentials"]["refresh_token"],
            token_uri=session["credentials"]["token_uri"],
            client_id=session["credentials"]["client_id"],
            client_secret=session["credentials"]["client_secret"]
        )
        service = build('gmail', 'v1', credentials=credentials)
        sender = 'me'
        to = data[0][0]['value']
        subject = data[0][1]['value']
        message_text = (data[0][2]['value']).strip()
        pdf_path = 'website/static/pdf/undergraduate_reg_export-' + fullname_addon + '.pdf'
        msg_w_pdf = create_message_with_attachment(sender, to, subject, message_text, pdf_path)
        send_message(service, 'me', msg_w_pdf)
        return '', 204
    elif (list(data_json)[0]) == 'draft':
        print('here')
        data = data_json[(list(data_json)[0])]
        fullname_addon = session['name'].replace(" ", "_")
        credentials = google.oauth2.credentials.Credentials(
            session["credentials"]["access_token"],
            refresh_token=session["credentials"]["refresh_token"],
            token_uri=session["credentials"]["token_uri"],
            client_id=session["credentials"]["client_id"],
            client_secret=session["credentials"]["client_secret"]
        )
        service = build('gmail', 'v1', credentials=credentials)
        sender = 'me'
        to = data[0][0]['value']
        subject = data[0][1]['value']
        message_text = (data[0][2]['value']).strip()
        pdf_path = 'website/static/pdf/undergraduate_reg_export-' + fullname_addon + '.pdf'
        msg_w_pdf = create_message_with_attachment(sender, to, subject, message_text, pdf_path)
        create_draft(service, 'me', msg_w_pdf)
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
            flash("Autofill Data Saved", "save")
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
                fullname_addon = session['name'].replace(" ","_")
                name, cred, courses = pdf.runfull(dictResults, p_data, fullname_addon)
                name = name.split('/')[-1]
                path = './static/pdf/' + name + "?v=" + str(time.time())
                delpath = 'website/static/pdf/' + name
                if p_data != [] and p_data[19] is not None:
                    fullp_name = p_data[0]+' '+p_data[1]
                    spdf.run(fullp_name, delpath)
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

def create_message_with_attachment(sender, to, subject, message_text, file):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    encoders.encode_base64(msg)
    fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    print(message)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    print(message)
    #message['raw'] = message['raw'].decode()
    #print(message)
    print('hello')
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def create_draft(service, user_id, message_body):
    """Create and insert a draft email. Print the returned draft's message and id.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_body: The body of the email message, including headers.

    Returns:
    Draft object, including draft id and message meta data.
    """
    try:
        message = {'message': message_body}
        draft = service.users().drafts().create(userId=user_id, body=message).execute()

        print('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))

        return draft
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None

