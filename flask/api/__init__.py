from flask_restx import Api

from .predict import predict_ns
from .train import train_ns

api = Api(title="Completion Rate API", version="1.0", description="Model Train & Prediction")

api.add_namespace(predict_ns)
api.add_namespace(train_ns)