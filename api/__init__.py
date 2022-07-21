import io, os, requests
from pathlib import Path
from re import I
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, jsonify, request
from flask_restful import Api, reqparse, abort, Resource
from keras.preprocessing import image
from keras.initializers import glorot_uniform


def create_app():
    app = Flask('api')

    # Config flask app
    app.debug = True
    app.config['SECRET_KEY'] = 'retinia'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    api = Api(app)

    # Define route with Resource
    api.add_resource(Prediction, '/')

    return app


# POST methode retourne un diagnostic
class Prediction(Resource):
    
    categories = {
        0 :'choroidal neovascularization', 
        1 :'diabetic macular edema', 
        2 :'drusen', 
        3 :'normal'
    }

    filename = ''

    def load_model(self):

        model = tf.keras.models.load_model(os.getcwd()+'\\api\\model\\retinal-oct-v100_1000.h5')
        model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

        return model

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

    def predict_result(self,img):
        Y_pred = self.load_model().predict(img)
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
    
    # GET method
    def get(self):
        return 'Retinal Diagnosis by Image-Based Deep Learning'
