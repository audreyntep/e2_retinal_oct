import io, os
from pathlib import Path
from re import I
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, jsonify, request
from flask_restful import Api, reqparse, abort, Resource
from keras.preprocessing import image


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


# POST retourne une prédiction
class Prediction(Resource):

    # loading model
    model = tf.keras.models.load_model(os.getcwd()+'\\api\\model\\retinal-oct.h5')

    categories = {
        0 : 'CNV', 
        1 : 'DME', 
        2 :'DRUSEN', 
        3 :'NORMAL'
    }

    def prepare_image(self, img):
        img = Image.open(io.BytesIO(img))
        img = img.resize((150, 150))
        img = np.array(img)
        img = np.expand_dims(img, 0)
        return img

    def predict_result(self,img):
        Y_pred = self.model.predict(img)
        return np.argmax(Y_pred, axis=1)

    def post(self):

        # prepare model
        self.model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

        # prepare file
        if 'file' not in request.files:
            return "Please try again. The Image doesn't exist"
        
        file = request.files.get('file')

        if not file:
            return

        img_bytes = file.read()
        img = self.prepare_image(img_bytes)


        return jsonify(prediction=self.predict_result(img))

    
    # fonction retournant un diagnostique
    def get(self):

        result =''

        self.model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

        file = request.files.get('file')
        print(type(file)) # <class 'werkzeug.datastructures.FileStorage'>
        img = self.prepare_image(file.read())
        print(img)

        #img = self.prepare_image(file.read())
        #print(img.shape)

        file = Path(os.getcwd()+"\\data\\DME-9583225-1.jpeg") #1
        #file = Path(os.getcwd()+"\\data\\CNV-6294785-1.jpeg") #0
        #file = Path(os.getcwd()+"\\data\\DRUSEN-9800172-2.jpeg") #2
        #file = Path(os.getcwd()+"\\data\\NORMAL-4872585-1.jpeg") #3
        #print(type(file)) #<class 'pathlib.WindowsPath'>

        # load image
        img = tf.keras.utils.load_img(file, target_size = (150, 150)) 
        print(img) # <PIL.Image.Image image mode=RGB size=150x150 at 0x1BA8D9B8EE0>

        # convert image to numpy 3D array
        img = tf.keras.utils.img_to_array(img)
        img = np.expand_dims(img, axis = 0)
        print(img.shape) # (1, 150, 150, 3)

        # return result as numpy int64
        result = np.argmax(self.model.predict(img))
        print(result)

        # return diagnosis as dict
        return {'diagnosis': self.categories.get(int(result))}

        #return 'Retinal Diagnosis by Image-Based Deep Learning'
