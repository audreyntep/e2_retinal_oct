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
        (0,'CNV : choroidal neovascularization'), 
        (1,'DME : diabetic macular edema'), 
        (2,'DRUSEN'), 
        (3,'NORMAL')
    ]
    reliability=87
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
        return render_template("home.html", categories=categories, reliability=reliability, diagnosis=diagnosis, oct_image=oct_image)

    if request.method  == 'POST':
        if 'diagnose' in request.form:
            print(request.form.get('diagnose'))
            print(__file__)
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
        else:
            diagnosis['error'] = "Please upload OCT image"

    return render_template("home.html", categories=categories, reliability=reliability, diagnosis=diagnosis)



