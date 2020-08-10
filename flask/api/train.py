import http.client

import redis
from flask_restx import Namespace, Resource, fields

from services import train

train_ns = Namespace('train', description='Model Training')

train_model = train_ns.model('Train', {
    'version': fields.Integer
})

r = redis.Redis()

@train_ns.route('')
class Train(Resource):
    @train_ns.doc('Train model')
    @train_ns.marshal_with(train_model, code=http.client.OK)
    def post(self):
        '''Train model'''
        return train.train()