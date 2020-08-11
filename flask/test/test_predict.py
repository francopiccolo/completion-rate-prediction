import unittest
import json

from app import create_app

with open('./test/data/predict_request.json') as f:
    REQUEST_BODY = json.load(f)

class TestPredict(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_prediction(self):
        response = self.client.post(
                    'predict',
                    data=json.dumps({'body': REQUEST_BODY}))

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.get_data(as_text=True))

        self.assertTrue('response_type' in response_json)

    def test_no_model(self):
        pass

    def test_bad_request(self):
        pass