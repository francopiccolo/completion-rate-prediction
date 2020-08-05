import pickle

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('./data/completion_rate.csv')

df['completion_rate'] = df['submissions'] / df['views']

features = [col for col in df.columns if col.startswith('feat')]
X = df[features]
y = df['completion_rate']

random_forest = RandomForestRegressor(n_estimators=10, max_depth=3)

print('Training model')
random_forest.fit(X, y)

pickle.dump(random_forest, open('./data/model.pkl', 'wb'))