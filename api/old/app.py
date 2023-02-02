#!/usr/bin/env python
# coding: utf-8

# import librairie
import io
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, request
import logging
logging.basicConfig(level=logging.DEBUG)


# load model
model_path = 'api/old/model/retinal-oct.h5'
model = tf.keras.models.load_model(model_path)


# prepare images 
def prepare_image(img):
    """
    prepares the image for the api call
    """
    img = Image.open(io.BytesIO(img)).convert('RGB')
    img = img.resize((150, 150))
    img = np.array(img)
    img = np.expand_dims(img, 0)
    return img


# prediction
def predict_result(img):
    """predicts the result"""
    return np.argmax(model.predict(img)[0])


# initialize flask object
app = Flask(__name__)


# setting up routes and their functions
@app.route('/predict', methods=['POST'])
def infer_image():
    logging.info(str(request.files))

    # Catch the image file from a POST request
    if 'file' not in request.files:
        return "Please try again. The Image doesn't exist"
    
    file = request.files.get('file')

    if not file:
        return

    # Read the image
    img_bytes = file.read()

    # Prepare the image
    img = prepare_image(img_bytes)

    # Return on a JSON format
    #return str(predict_result(img))
    return {'result': str(predict_result(img))}
    

@app.route('/', methods=['GET'])
def index():
    return 'Retinal OCT prediction API'


# run the API
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',  use_reloader=False)
    






