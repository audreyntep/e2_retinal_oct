import os, json
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from werkzeug.datastructures import FileStorage
import logging
logging.basicConfig(level=logging.DEBUG)

# define model to use
global model_name
#model_name = 'vE10-B64'
model_name = 'vgg16_e10b64_6'

def create_app():
    global app
    app = Flask('api')

    # Config flask app
    app.debug = True
    app.config['SECRET_KEY'] = 'retinia'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    api = Api(app)

    # Define route with Resource
    api.add_resource(Home, '/')
    api.add_resource(Prediction, '/diagnosis')
    api.add_resource(ModelLoader, '/model')
    api.add_resource(Metrics, '/metrics')
    api.add_resource(Diagnosis, '/classes')

    return app


# '/'
class Home(Resource):

    def get(self):
        return 'Retinal OCT prediction API'

# '/metrics'
class Metrics(Resource):

    # return json
    def get(self):
        data = open(os.getcwd()+'/api/model/'+model_name+'/retinal_oct_model_'+model_name+'_eval.json')
        return json.load(data)
    
# '/model'
class ModelLoader(Resource):

    # model paths
    model_h5_path = 'retinal_oct_model_'+model_name+'.h5'
    model_json_path = 'retinal_oct_model_'+model_name+'.json'
    __model = None

    # return keras model
    def __init__(self):
        # getting h5 path
        model_h5 = os.getcwd()+'/api/model/'+model_name+'/'+self.model_h5_path
        # loading model with kears
        self.__model = tf.keras.models.load_model(model_h5)
        self.__model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

    # return prediction
    def predict(self, img):
        return self.__model.predict(img)
    
    # return json
    def get(self):
        data = open(os.getcwd()+'/api/model/'+model_name+'/'+self.model_json_path)
        return json.load(data)


# '/classes'
class Diagnosis(Resource):

    classes = {
        0 :'choroidal neovascularization (CNV)', 
        1 :'diabetic macular edema (DME)', 
        2 :'drusen', 
        3 :'normal'
    }

    filename = ''

    def get_filename(self):
        return self.filename

    @staticmethod
    def prepare_image(file):
        filename = file.filename
        img_path = os.path.join(os.getcwd(), 'api', 'data', 'diagnoses', filename)
        # open image
        img = Image.open(file.stream)
        # save image
        img.save(img_path)
        # load image
        img = tf.keras.utils.load_img(img_path, target_size=(150, 150))
        # resize image
        img = tf.keras.utils.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        return img, filename


    @staticmethod
    def get_result(file: FileStorage):
        # parameter byte object
        img, filename = Diagnosis.prepare_image(file)
        # load model
        model_loader = ModelLoader()
        # predict
        Y_pred = np.argmax(model_loader.predict(img), axis=1)
        # transform result nd numpy array to list
        result = np.ndarray.tolist(Y_pred)

        # format diagnosis
        return {
            'filename': filename,
            'result': json.dumps(result[0]),
            'classe': Diagnosis.classes.get(int(result[0]))
        }

    # return json
    def get(self):
        return jsonify(self.classes)


# '/diagnosis' POST methode retourne un diagnostic
class Prediction(Resource):

    # POST method retun diagnosis in json
    def post(self):

        diagnoses = []
        try :
            files = request.files.getlist('file')
            # for each file get diagnosis
            for file in files :
                diagnoses.append(Diagnosis.get_result(file))
            # return error if no image
            if diagnoses == []:
                return {400 : "No image found."}
            # return diagnosis as json
            return jsonify(diagnoses)
        
        except Exception as e:
            print(e)
            return {418 : "Please try again."}


    
        
