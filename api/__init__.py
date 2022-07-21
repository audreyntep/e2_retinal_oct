import os, json
from re import I
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

# define model to use
global model_name
model_name = 'vE10-B64'

def create_app():
    app = Flask('api')

    # Config flask app
    app.debug = True
    app.config['SECRET_KEY'] = 'retinia'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    api = Api(app)

    # Define route with Resource
    api.add_resource(Prediction, '/')
    api.add_resource(Model, '/model')

    return app
    

class Model(Resource):

    def __init__(self) -> None:
        super().__init__()

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
    def data_model(self):
        data = open(os.getcwd()+'/api/model/'+model_name+'/'+self.model_json_path)
        return json.load(data)


# POST methode retourne un diagnostic
class Prediction(Resource):
    
    categories = {
        0 :'choroidal neovascularization', 
        1 :'diabetic macular edema', 
        2 :'drusen', 
        3 :'normal'
    }

    filename = ''

    # Filestorage as input, Image object as output
    def prepare_image(self, file):

        self.filename = file.filename
        img_path = 'api/data/'+self.filename

        # open image
        img = Image.open(file.stream)
        # save image
        img.save(img_path)
        # load image
        img = tf.keras.utils.load_img(img_path, target_size = (150, 150)) 
        # resize image
        img = tf.keras.utils.img_to_array(img)
        img = np.expand_dims(img, axis = 0)
 
        #img = Image.open(io.BytesIO(img))
        #img = img.resize((150, 150))
        #img = np.array(img)
        #img = np.expand_dims(img, axis = 0)

        return img

    # Image object as input, return numpy array prediction
    def predict_result(self,img):
        Y_pred = Model().load_model().predict(img)
        return np.argmax(Y_pred, axis=1)


    # POST method retun diagnosis in json
    def post(self):

        # prepare file
        if 'file' not in request.files:
            return "Please try again. The Image doesn't exist"
        file = request.files.get('file')

        # prepare image
        if not file:
            return
        img = self.prepare_image(file)

        # return result as numpy int64
        result = self.predict_result(img)

        # return diagnosis as json
        return jsonify(diagnosis={'filename': self.filename, 'result': self.categories.get(int(result[0]))})
    

    # GET method return model architecture and metrics as json
    def get(self):
        #return 'Retinal Diagnosis by Image-Based Deep Learning'
        return Model().data_model()
