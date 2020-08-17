from flask_restx import Api

from .predict import predict_ns
from .train_predict import train_predict_ns

api = Api(title='Completion Rate API',
          version='1.0',
          description="""With this API you can train a model for forms completion rate prediction and run predictions.\n\nThe model trained is a Random Forest with max_depth = 20 and n_estimators = 30 based on 47 numerical features feat_XX.""")

api.add_namespace(predict_ns)
api.add_namespace(train_predict_ns)