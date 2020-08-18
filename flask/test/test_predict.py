import unittest
from unittest import mock
import json

import fakeredis

from app import create_app

with open('./test/data/request_prediction.json') as f:
    REQUEST_PREDICTION = json.load(f)

with open('./test/data/request_missing_features.json') as f:
    REQUEST_MISSING_FEATURES = json.load(f)

with open('./test/data/request_not_float.json') as f:
    REQUEST_NOT_FLOAT = json.load(f)

with open('./test/data/request_smaller_than_0.json') as f:
    REQUEST_SMALLER_THAN_0 = json.load(f)

class TestPredict(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        redis_patcher = mock.patch('services.predict.redis.Redis', fakeredis.FakeRedis)
        self.redis = redis_patcher.start()

    def tearDown(self):
        self.app_context.pop()

    def submit_request(self, request_body):
        return self.client.post(
                    'predict',
                    headers={'content-type': 'application/json'},
                    data=json.dumps(request_body))

    def test_prediction(self):
        response = self.submit_request(REQUEST_PREDICTION)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data)
        self.assertIsInstance(response_json['response']['prediction'], float)
        self.assertEqual(response_json['response_type'], 'Successful prediction')

    def test_no_model(self):
        self.app.config['MODEL_FILE_PATH'] = ''
        response = self.submit_request(REQUEST_PREDICTION)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data)
        self.assertEqual(response_json['response_type'], 'There is no model')

    def test_no_json(self):
        response = self.client.post(
            'predict',
            headers={'content-type': 'text'},
            data=json.dumps(REQUEST_PREDICTION))
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['response_type'], 'Not json')

        response = self.client.post(
                    'predict',
                    headers={'content-type': 'application/json'},
                    data='Not json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertEqual(response_json['response_type'], 'Not json')

    def test_missing_features(self):
        response = self.submit_request(REQUEST_MISSING_FEATURES)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data)
        self.assertEqual(response_json['response_type'], 'Missing features')

    def test_features_type(self):
        response = self.submit_request(REQUEST_NOT_FLOAT)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data)
        self.assertEqual(response_json['response_type'], 'Some features are not floats')

    def test_features_values(self):
        response = self.submit_request(REQUEST_SMALLER_THAN_0)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data)
        self.assertEqual(response_json['response_type'], 'Some features are not in expected range')