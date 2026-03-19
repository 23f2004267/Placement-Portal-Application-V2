import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "placement.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "placement_secret_key"

    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 60