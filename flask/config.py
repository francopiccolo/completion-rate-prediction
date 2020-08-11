import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class BaseConfig:
    DATASET_FILE_PATH = os.path.join(basedir, os.getenv('DATASET_FILE_PATH'))

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

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}