from re import U
from flask import Flask, Blueprint, render_template, request
import requests

views = Blueprint('views', __name__)

def create_app():
    app = Flask('web')

    # Config flask app
    app.debug = True

    # Define route with Blueprint
    app.register_blueprint(views, url_prefix='/')

    return app

@views.route('/', methods=['GET','POST'])
def home():

    categories = [
        (0,'CNV : choroidal neovascularization'), 
        (1,'DME : diabetic macular edema'), 
        (2,'DRUSEN'), 
        (3,'NORMAL')
    ]
    diagnosis = ''


    if request.method  == 'POST':
        # récupération des paramètres URL et envoi d'une requête de prédiction à l'api
        r = requests.post(
            url='http://127.0.0.1:5000/api', 
            files = {
                'oct':request.form.get('load'),
            })
        diagnosis = ''

        return render_template("home.html", categories=categories, reliability=87, diagnosis=diagnosis)

    return render_template("home.html", categories=categories, reliability=87, diagnosis=diagnosis)



