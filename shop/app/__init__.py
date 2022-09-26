"""
This contains the application factory for creating flask application instances.
Using the application factory allows for the creation of flask applications configured
for different environments based on the value of the CONFIG_TYPE environment variable
"""

import os

import click
from flask import Flask, render_template, redirect, url_for, flash
from db import db
from .management.create_admin import create_admin
from .utils.extensions import cache, csrf, mail, migrate, security, celery


### Application Factory ###
def create_app():
    app = Flask(__name__)

    # Configure the flask app instance
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

    # Initialize SQLAlchemy object
    from db import db_init
    db_init(app)

    # Register blueprints
    register_blueprints(app)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Configure celery
    from .utils.extensions import celery

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    @app.cli.command("create_admin")
    @click.argument('username', required=False)
    @click.argument('email', required=False)
    @click.argument('password', required=False)
    def load_admin(username=None, email=None, password=None):
        """
        Create admin user with custom params. create_admin ['username', 'email', 'password]
        """
        create_admin(username, email, password)

    return app


### Helper Functions ###
def register_blueprints(app):
    from .auth import auth_blueprint
    from .main import main_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)


def initialize_extensions(app):
    # flask-admin extension
    from .utils import init_admin
    init_admin(app)

    # flask_wtf CSRFProtect extension
    cache.init_app(app)

    # flask_wtf CSRFProtect extension
    csrf.init_app(app)

    # flask_mail extension
    mail.init_app(app)

    # flask-migrate extension
    migrate.init_app(app, db)

    # flask-security
    from .utils import init_security
    init_security(app)


def register_error_handlers(app):
    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error/400.html'), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error/403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('error/405.html'), 405

    # 405 - Method Not Allowed
    @app.errorhandler(413)
    def request_entity_too_large(e):
        flash('413: Request Entity Too Large', 'danger')
        return redirect('/', 302)

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('error/500.html'), 500


def configure_logging(app):
    pass


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config.get('CELERY_BROKER_URL')
    celery.conf.beat_schedule = app.config['BEAT_SCHEDULE']


    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
