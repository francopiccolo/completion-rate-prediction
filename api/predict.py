import http.client

from flask import request
from flask_restx import Namespace, Resource, fields

from services import predict

predict_ns = Namespace('predict', description='Model Prediction')

predict_model = predict_ns.model('Predict', {
    'prediction': fields.Float
})

@predict_ns.route('')
class Predict(Resource):
    @predict_ns.doc('Predict model')
    @predict_ns.marshal_with(predict_model, code=http.client.OK)
    def post(self):
        '''Predict'''
        return predict.predict(request.json)