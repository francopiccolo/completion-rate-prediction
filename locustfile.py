import json
from locust import HttpUser, task, between, constant

class Trainer(HttpUser):
    wait_time = constant(1500*10)

    @task
    def train(self):
        self.client.post('train')

with open('./test/data/predict_request.json') as f:
    predict_request_body = json.load(f)
print('Request body', predict_request_body)
class Predictor(HttpUser):
    weight = 1500*10
    wait_time = between(5, 10)

    @task
    def predict(self):
        headers = {'content-type': 'application/json'}
        self.client.post('predict',
                         data=json.dumps(predict_request_body),
                         headers=headers)