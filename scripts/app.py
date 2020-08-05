import pickle

import pandas as pd

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    request_json = request.json
    print('Request:', request_json)
    request_df = pd.DataFrame(request_json, index=[0])
    prediction = model.predict(request_df)[0]
    return jsonify({'prediction': str(prediction)})

if __name__ == '__main__':
    model = pickle.load(open('./data/model.pkl', 'rb'))
    print('Model loaded')
    app.run(debug=True, host='0.0.0.0')