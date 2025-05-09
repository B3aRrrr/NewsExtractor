import os

basedir = os.path.abspath((os.path.dirname(__file__)))

class Config:
    DATASETS_FOLDER=os.path.join(basedir,'datasets')

# class DevelopmentConfig(Config):
#     DEBUG = True
#     MAIL_SERVER = 'smtp.googlemail.com'
#     MAIL_PORT =587
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
#     MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
#     SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir,"sqlite","data-dev.db")}'
    
# class TestingConfig(Config):
#     TESTING=True
#     SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir,"sqlite","data-test.db")}'

# class ProductionConfig(Config):
#     TESTING=True
#     SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir,"sqlite","data.db")}'

config = {
    
    'default':Config
}