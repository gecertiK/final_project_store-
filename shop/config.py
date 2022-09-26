#  Flask Configuration file

#!/usr/bin/env python

import os
from dotenv import load_dotenv

from beat_schedule import BEAT_SCHEDULE

load_dotenv()

# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """
    # Default settings
    HOST = os.getenv('HOST', default='127.0.0.1')
    PORT = os.getenv('PORT', default=5000)
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    TIMEZONE = 'Europe/Kiev'

    # Settings applicable to all environments

    # Generate a nice key using secrets.token_urlsafe()
    SECRET_KEY = os.getenv("SECRET_KEY")
    # Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
    # Generate a good salt using: secrets.SystemRandom().getrandbits(128)
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    SECURITY_SEND_REGISTER_EMAIL = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', default='')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', default='')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', default='')
    MAIL_SUPPRESS_SEND = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery
    task_serializer = 'json'
    CELERY_BROKER_URL = os.getenv('AMQP_URL')
    include = ["app.main.tasks.tasks"]

    RESULT_BACKEND = os.getenv('REDIS_URL')

    BEAT_SCHEDULE = BEAT_SCHEDULE

    # Cache
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.getenv('REDIS_CACHE')
    CACHE_DEFAULT_TIMEOUT = 150

    # flask_security
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True

    # flask_admin
    FLASK_ADMIN_SWATCH = 'cerulean'


class DevelopmentConfig(Config):
    DEBUG = True

    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'test.db')


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', default="sqlite:///" + os.path.join(basedir, 'prod.db'))
