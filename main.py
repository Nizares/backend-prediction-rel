import os
from flask import Flask, request, jsonify, json, make_response
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Sequential
from tensorflow.keras import optimizers, losses, activations, models
from tensorflow.keras.layers import Convolution2D, Dense, Input, Flatten, Dropout, MaxPooling2D, BatchNormalization, GlobalAveragePooling2D, Concatenate
from tensorflow.keras.applications import InceptionV3
import numpy as np
import tensorflow as tf
import tempfile

app = Flask(__name__)
lists = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

base_model = InceptionV3(weights='imagenet', 
                                include_top=False, 
                                input_shape=(150,150,3))

add_model = Sequential()
add_model.add(base_model)
add_model.add(GlobalAveragePooling2D())
add_model.add(tf.keras.layers.Dense(512, activation='relu'))
add_model.add(tf.keras.layers.Dense(256, activation='relu'))
add_model.add(Dropout(0.5))      
add_model.add(Dense(26, activation='softmax'))

model = add_model
model.compile(loss='categorical_crossentropy', 
              optimizer=optimizers.Adam(learning_rate=1e-4),
              metrics=['accuracy'])

model.load_weights("./model_weights.h5")

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route("/predict", methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file part in the request'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)
    

    image = tf.keras.preprocessing.image.load_img(temp_file.name, target_size=(150, 150))
    x = tf.keras.preprocessing.image.img_to_array(image)
    x = x / 255.0
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    pred = model.predict(images)
    preds = lists[np.argmax(pred)]
    id = np.argmax(pred) + 1

    score = np.round(np.max(pred), 3)
    
    temp_file.close()

    response = {   
        "message": "success",
        "result": preds,
        "id": id.tolist(),
        "score" : score.tolist()
    }
    
    if score > 0.5 and score <= 1.0:
        # return prediction
        return jsonify(response)
    else:
        return jsonify({"message": "predict failed"})

if __name__ == "__main__":
    app.run(port=8080, debug=True)