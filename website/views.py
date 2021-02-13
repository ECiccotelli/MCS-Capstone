from flask import Blueprint, render_template
#Blueprints are use to organize the different pages on a web app.
#The blueprint is connected in the setup of the init.py file

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('dashboard.html')