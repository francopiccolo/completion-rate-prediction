import os
import pickle

import redis
import pandas as pd
from flask import current_app

r = redis.Redis(decode_responses=True)

model = None
model_version = None

def predict(request_json):
    global model, model_version
    model_file_path = current_app.config['MODEL_FILE_PATH']

    if not model:
        if os.path.isfile(model_file_path):
            model_version = r.get('model_version')
            # here the training process may finish causing trouble
            model = load_model(model_file_path)
        else:
            return {'prediction': 0}

    current_app.logger.info(f'{model_version} is the current model')
    latest_model_version = r.get('model_version')
    current_app.logger.info(f'{latest_model_version} is the latest model')

    if model_version != latest_model_version:
        model = load_model(model_file_path)
        model_version = latest_model_version

    request_df = pd.DataFrame(request_json, index=[0])
    prediction = model.predict(request_df)[0]
    return {'prediction': prediction}

def load_model(model_file_path):
    return pickle.load(open(model_file_path, 'rb'))