import os
import json
import pickle

import redis
import pandas as pd
from flask import current_app

model = None
model_version = None

def predict(request):
    if not _is_json(request):
        response_type = 'Not json'
        return _response(response_type, None)

    request_json = request.json

    if not _contains_all_features(request_json):
        response_type = 'Missing features'
        return _response(response_type, None)

    if not _features_can_be_float(request_json):
        response_type = 'Some features are not floats'
        return _response(response_type, None)

    if not _features_in_range(request_json):
        response_type = 'Some features are not in expected range'
        return _response(response_type, None)

    request_json = {k:v for k, v in request.json.items() if k in current_app.config['FEATURES']}

    current_app.logger.info(request_json)

    r = redis.Redis(host=current_app.config['REDIS_HOST'],
                    decode_responses=True)

    global model, model_version
    model_file_path = current_app.config['MODEL_FILE_PATH']

    if not model:
        if os.path.isfile(model_file_path):
            model_version = r.get('model_version')
            model = _load_model(model_file_path) # potential paralell issue
        else:
            response_type = 'There is no model'
            return _response(response_type, None)

    current_app.logger.info(f'{model_version} is the current model')
    latest_model_version = r.get('model_version')
    current_app.logger.info(f'{latest_model_version} is the latest model')

    if model_version != latest_model_version:
        model = _load_model(model_file_path)
        model_version = latest_model_version

    request_df = pd.DataFrame(request_json, index=[0])

    response_type = 'Successful prediction'
    prediction = model.predict(request_df)[0]
    response = {'prediction': prediction,
                'model_version': model_version}
    current_app.logger.info(f'Prediction: {response}')
    return _response(response_type, response)

def _is_json(request):
    if not request.is_json:
        return False
    try:
        json_object = json.loads(request.data)
    except ValueError as e:
        return False

    return True

def _contains_all_features(request_json):
    if all(feature in request_json for feature in current_app.config['FEATURES']):
        return True
    return False

def _features_can_be_float(request_json):
    for feature in current_app.config['FEATURES']:
        try:
            feature_float = float(request_json[feature])
        except ValueError as e:
            return False
    return True

def _features_in_range(request_json):
    if all(float(request_json[feature]) >= 0 for feature in current_app.config['FEATURES']):
        return True
    return False

def _load_model(model_file_path):
    return pickle.load(open(model_file_path, 'rb'))

def _response(response_type, response):
    return {
        'response_type': response_type,
        'response': response,
    }