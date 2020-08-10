import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class BaseConfig:
    DATASET_FILE_PATH = os.path.join(basedir, os.getenv('DATASET_FILE_PATH'))
    MODEL_FILE_PATH = os.path.join(basedir, os.getenv('MODEL_FILE_PATH'))

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    REDIS_HOST = os.getenv('DEV_REDIS_HOST')

class TestingConfig(BaseConfig):
    TESTING = True

class ProductionConfig(BaseConfig):
    REDIS_HOST = os.getenv('PROD_REDIS_HOST')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}