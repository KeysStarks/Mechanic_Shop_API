import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{DB_PASSWORD}@localhost/mechanic_shop_db'
    
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:testing.db'
    DEBUG = True
    CACHE_TYPE = 'NullCache'
    RATELIMIT_ENABLED = False
    
class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = "SimpleCache"