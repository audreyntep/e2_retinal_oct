import os, json
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

# define model to use
global model_name
#model_name = 'vE10-B64'
model_name = 'vgg16_e10b64_6'

def create_app():
    app = Flask('api')

    # Config flask app
    app.debug = True
    app.config['SECRET_KEY'] = 'retinia'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    api = Api(app)

    # Define route with Resource
    api.add_resource(Home, '/')
    api.add_resource(Prediction, '/diagnosis')
    api.add_resource(Model, '/model')
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
class Model(Resource):

    # model paths
    model_h5_path = 'retinal_oct_model_'+model_name+'.h5'
    model_json_path = 'retinal_oct_model_'+model_name+'.json'

    # return keras model
    def load_model(self):
        # getting h5 path
        model_h5 = os.getcwd()+'/api/model/'+model_name+'/'+self.model_h5_path
        # loading model with kears
        model = tf.keras.models.load_model(model_h5)
        model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

        return model

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

    # Filestorage as input, Image object as output
    def prepare_image(self, file):

        self.filename = file.filename
        img_path = 'api/data/diagnoses/'+self.filename

        # open image
        img = Image.open(file.stream)

        # save image
        img.save(img_path)
        # load image
        img = tf.keras.utils.load_img(img_path, target_size = (150, 150)) 
        # resize image
        img = tf.keras.utils.img_to_array(img)
        img = np.expand_dims(img, axis = 0)

        return img

    # Image object as input, return numpy array prediction
    def predict_result(self,img):
        Y_pred = Model().load_model().predict(img)
        return np.argmax(Y_pred, axis=1)


    # Filestorage as input, return dict
    def get_result(self, file):
        # parameter byte object
        img = self.prepare_image(file)

        # transform result nd numpy array to list
        result = np.ndarray.tolist(self.predict_result(img))

        # format diagnosis
        return {
            'filename': self.filename, 
            'result': json.dumps(result[0]),
            'classe': self.classes.get(int(result[0]))
            }

    # return json
    def get(self):
        return jsonify(self.classes)


# '/diagnosis' POST methode retourne un diagnostic
class Prediction(Resource):

    # POST method retun diagnosis in json
    def post(self):

        diagnoses = []

        # prepare file
        if len(request.files.getlist('file')) < 1 :
            return {204 : "Please try again. The Image doesn't exist"}
        files = request.files.getlist('file')

        if not files:
            return {204 : "Please try again. The Image doesn't exist"}

        for f in files :
            diagnoses.append(Diagnosis().get_result(f))
        print(diagnoses)
        # return diagnosis as json
        return jsonify(diagnosis=diagnoses)
    

    # GET method return model architecture and metrics as json
    def get(self):
        return 'Retinal Diagnosis by Image-Based Deep Learning'
        
