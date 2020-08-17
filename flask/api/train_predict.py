import http.client

import redis
from flask import request
from flask_restx import Namespace, Resource, fields

from services import train, predict
from api.predict import request_model, response_model

train_predict_ns = Namespace('train_predict', description='Train model and make a prediction')

r = redis.Redis()

@train_predict_ns.route('')
class Train(Resource):
    @train_predict_ns.expect(request_model)
    @train_predict_ns.marshal_with(response_model, code=http.client.OK, description='Successful prediction')
    def post(self):
        train.train()
        return predict.predict(request)