import pickle

import redis
from flask import current_app
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def train():
    r = redis.Redis(host=current_app.config['REDIS_HOST'])

    df = pd.read_csv(current_app.config['DATASET_FILE_PATH'])

    df['completion_rate'] = df['submissions'] / df['views']

    features = [col for col in df.columns if col.startswith('feat')]
    X = df[features]
    y = df['completion_rate']

    random_forest = RandomForestRegressor(n_estimators=10, max_depth=3)
    random_forest.fit(X, y)

    pickle.dump(random_forest, open(current_app.config['MODEL_FILE_PATH'], 'wb'))

    current_app.logger.info('Training model')

    r.incr('model_version')
    model_version = r.get('model_version')

    return {'response_type': 'Trained succesfully',
            'response': {'model_version': model_version}}