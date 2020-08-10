from flask import Flask

from config import config
from api import api

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    api.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0')