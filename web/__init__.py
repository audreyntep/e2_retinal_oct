from re import U
import os
from pathlib import Path
from flask import Flask, Blueprint, render_template, request, url_for
import requests
from PIL import Image

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
        ('choroidal neovascularization (CNV)'), 
        ('diabetic macular edema (DME)'), 
        ('drusen'), 
        ('normal')
    ]
    accuracy=90.50
    diagnosis={}

    # prepare file
    if 'oct_file' in request.files and request.files.get('oct_file'):
        file = request.files.get('oct_file')

        # open image
        img = Image.open(file.stream)

        # save image
        img.save('web/static/oct_image/'+file.filename)

        oct_image={
            'name': file.filename,
            'url' : url_for('static', filename='oct_image/'+file.filename)
        }
        return render_template("home.html", categories=categories, accuracy=str(accuracy), oct_image=oct_image)

    if request.method  == 'POST':
        if 'diagnose' in request.form:

            # send image to api for diagnosis
            r = requests.post(
                url='http://127.0.0.1:5000/api', 
                files = {
                    'file': open('web/'+request.form.get('diagnose'),'rb')
                })
            
            # return diagnosis if response is True (status code under 400)
            diagnosis = r.json().get('diagnosis') if r.ok else ''
            if diagnosis != '':
                diagnosis['url'] = url_for('static', filename='oct_image/'+diagnosis.get('filename'))
            
            return render_template("home.html", categories=categories, accuracy=str(accuracy), diagnosis=diagnosis)

    return render_template("home.html", categories=categories, accuracy=str(accuracy))



