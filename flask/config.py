import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class BaseConfig:
    DATASET_FILE_PATH = os.path.join(basedir, os.getenv('DATASET_FILE_PATH'))
    FEATURES = ['feat_' + str(i).zfill(2) for i in range(1, 48)]
    N_ESTIMATORS = 20
    MAX_DEPTH = 20

    def init_app(app):
        pass

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    REDIS_HOST = os.getenv('DEV_TEST_REDIS_HOST')
    MODEL_FILE_PATH = os.path.join(basedir, os.getenv('DEV_PROD_MODEL_FILE_PATH'))

class TestingConfig(BaseConfig):
    TESTING = True
    REDIS_HOST = os.getenv('DEV_TEST_REDIS_HOST')
    MODEL_FILE_PATH = os.path.join(basedir, os.getenv('TEST_MODEL_FILE_PATH'))

class ProductionConfig(BaseConfig):
    REDIS_HOST = os.getenv('PROD_REDIS_HOST')
    MODEL_FILE_PATH = os.path.join(basedir, os.getenv('DEV_PROD_MODEL_FILE_PATH'))

    def init_app(app):
        import logging
        app.logger.setLevel(logging.DEBUG)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}