import os
import pickle

import redis
import pandas as pd
from flask import current_app

model = None
model_version = None

def predict(request_json):
    r = redis.Redis(host=current_app.config['REDIS_HOST'],
                    decode_responses=True)

    current_app.logger.info(request_json)

    global model, model_version
    model_file_path = current_app.config['MODEL_FILE_PATH']

    if not model:
        if os.path.isfile(model_file_path):
            if r.exists('model_version'):
                model_version = r.get('model_version')
            else:
                model_version = 0
            # here the training process may finish causing trouble
            model = load_model(model_file_path)
        else:
            response_type = 'There is no model'
            return _response(response_type, None)

    current_app.logger.info(f'{model_version} is the current model')
    latest_model_version = r.get('model_version')
    current_app.logger.info(f'{latest_model_version} is the latest model')

    if model_version != latest_model_version:
        model = load_model(model_file_path)
        model_version = latest_model_version

    request_df = pd.DataFrame(request_json, index=[0])

    response_type = 'Successful prediction'
    prediction = model.predict(request_df)[0]
    response = {'prediction': prediction,
                'model_version': model_version}
    current_app.logger.info(f'Prediction: {response}')
    return _response(response_type, response)

def load_model(model_file_path):
    return pickle.load(open(model_file_path, 'rb'))

def _response(response_type, response):
    return {
        'response_type': response_type,
        'response': response,
    }