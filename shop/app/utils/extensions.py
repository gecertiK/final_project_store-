"""Extensions registry
All extensions here are used as singletons and
initialized in application factory
"""
from flask_admin import Admin
# from flask_caching import Cache
from flask_caching import Cache
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import Security
from flask_wtf import CSRFProtect
from celery import Celery

from config import Config

admin = Admin()
cache = Cache()
csrf = CSRFProtect()
mail = Mail()
migrate = Migrate()
security = Security()
celery = Celery(include=Config.include)
