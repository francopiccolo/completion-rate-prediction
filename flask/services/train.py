import pickle

import redis
from flask import current_app
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def train():
    r = redis.Redis(host=current_app.config['REDIS_HOST'])

    df = pd.read_csv(current_app.config['DATASET_FILE_PATH'])

    df['completion_rate'] = df['submissions'] / df['views']

    X = df[current_app.config['FEATURES']]
    y = df['completion_rate']

    random_forest = RandomForestRegressor(
                        n_estimators=current_app.config['N_ESTIMATORS'],
                        max_depth=current_app.config['MAX_DEPTH'])

    current_app.logger.info('Training model')
    random_forest.fit(X, y)
    current_app.logger.info('Model trained')

    pickle.dump(random_forest, open(current_app.config['MODEL_FILE_PATH'], 'wb'))
    r.incr('model_version')