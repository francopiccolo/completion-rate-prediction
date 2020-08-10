import http.client

from flask import request
from flask_restx import Namespace, Resource, fields

from services import predict

predict_ns = Namespace('predict', description='Model Prediction')

prediction_model = predict_ns.model('Prediction', {
        'model_version': fields.Integer,
        'prediction': fields.Float,
})

response_model = predict_ns.model('Predict', {
    'response_type': fields.String,
    'response': fields.Nested(prediction_model, skip_none=True)
})

@predict_ns.route('')
class Predict(Resource):
    @predict_ns.doc('Predict model')
    @predict_ns.marshal_with(response_model, code=http.client.OK, skip_none=True)
    def post(self):
        '''Predict'''
        return predict.predict(request.json)