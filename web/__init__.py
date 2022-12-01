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

def get_model():
    r = requests.get(url='http://127.0.0.1:5000/api/model')
    return r.json()

def get_metrics():
    r = requests.get(url='http://127.0.0.1:5000/api/metrics')
    return r.json()

def get_classes():
    r = requests.get(url='http://127.0.0.1:5000/api/classes')
    return r.json()

def get_color(key):
    color = {
        0 : 'firebrick',
        1 : 'firebrick',
        2 : 'orangered',
        3 : 'forestgreen'
     }
    if key in color.keys() :
        return color.get(key)


@views.route('/', methods=['GET','POST'])
def home():

    # get CNN classes
    classes = []
    for c in get_classes().values():
        classes.append(c)

    # get CNN accuracy
    accuracy=round(get_metrics().get('accuracy')*100,2)

    # prepare file
    if 'oct_file' in request.files and request.files.get('oct_file'):

        files = request.files.getlist('oct_file')
        oct_images = []

        for file in files:
            # open image
            img = Image.open(file.stream)
            # save image
            img.save('web/static/oct_image/'+file.filename)
            # store data to show image
            oct_images.append({
                'name': file.filename,
                'url' : url_for('static', filename='oct_image/'+file.filename)
            })

        return render_template("home.html", classes=classes, accuracy=str(accuracy), oct_images=oct_images)

    if request.method  == 'POST':

        # define request content
        urls=[]
        for url in request.form.getlist('oct_image') :
            urls.append(('file', open('web'+url, 'rb')))

        if 'diagnose' in request.form:

            # send image to api for diagnosis
            r = requests.post(
                url='http://127.0.0.1:5000/api', 
                files = urls,
                )
            
            # return diagnosis if response is True (status code under 400)
            diagnosis = []
            diagnosis = r.json().get('diagnosis') if r.ok else ''
            if len(diagnosis) > 0 :
                for i in range(0,len(diagnosis)):
                    diagnosis[i].update({'url': url_for('static', filename='oct_image/'+diagnosis[i].get('filename'))})
                    diagnosis[i].update({'style': 'color:'+ str(get_color(int(diagnosis[i].get('result')))) })
            
            return render_template("home.html", classes=classes, accuracy=str(accuracy), diagnosis=diagnosis)

    return render_template("home.html", classes=classes, accuracy=str(accuracy))



