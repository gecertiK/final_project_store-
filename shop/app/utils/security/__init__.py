# security
from flask import url_for
from flask_security import SQLAlchemyUserDatastore
from app.models import User, Role
from db import db
from app.utils.extensions import security
from .forms import SignUpForm
from ..extensions import admin
from flask_admin import helpers as admin_helpers

### Instantiate Security ###
# from .utils import MyMailUtil

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


# Security instance initiation
def init_security(app):
    security.init_app(app, user_datastore, register_form=SignUpForm)

    # @security.context_processor
    # def security_context_processor():
    #     return dict(
    #         admin_base_template=admin.base_template,
    #         admin_view=admin.index_view,
    #         h=admin_helpers,
    #         get_url=url_for
    #     )