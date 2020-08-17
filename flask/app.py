from flask import Flask

from config import config
from api import api

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    api.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0')