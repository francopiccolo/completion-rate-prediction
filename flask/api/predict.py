import http.client

from flask import request
from flask_restx import Namespace, Resource, fields

from config import BaseConfig
from services import predict

predict_ns = Namespace('predict', description='Make a prediction')
request_body = {feature: fields.Float(required=True, min=0) for feature in BaseConfig.FEATURES}
request_model = predict_ns.model('Predict request', request_body)
prediction_model = predict_ns.model('Prediction', {
        'model_version': fields.Integer,
        'prediction': fields.Float,
})

response_model = predict_ns.model('Predict response', {
    'response_type': fields.String,
    'response': fields.Nested(prediction_model, skip_none=True)
})

@predict_ns.route('')
class Predict(Resource):
    @predict_ns.expect(request_model)
    @predict_ns.marshal_with(response_model, code=http.client.OK, skip_none=True)
    def post(self):
        return predict.predict(request)