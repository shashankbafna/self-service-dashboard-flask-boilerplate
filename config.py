import os

class Config:
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    SELFSERVICE_TYPE = os.environ.get('SELFSERVICE_TYPE', 'MASTER')
    LOG_FILE = os.environ.get('LOG_FILE', 'selfservice.log')
    BITBUCKET_API_BASE_URL = 'https://api.bitbucket.org/2.0/repositories/YOUR_REPO_NAME'
    BITBUCKET_USERNAME = 'YOUR_USERNAME'
    BITBUCKET_PASSWORD = 'YOUR_PASSWORD'
    MASTER_BEARER_TOKEN = os.environ.get('MASTER_BEARER_TOKEN', 'your_master_bearer_token')
    MASTER_URL = os.environ.get('MASTER_URL', 'http://localhost:5000')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False