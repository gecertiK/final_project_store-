from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from flask import redirect, url_for, flash, abort


class AdminHomeView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_active and current_user.is_authenticated:
            if 'admin' in current_user.roles:
                return True
            else:
                abort(403)
        else:
            return False

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login')+'?next=/admin/')


class RoleModelAdmin(ModelView):
    column_list = ('name', 'description', 'permissions')
    # create_modal = True

    def is_accessible(self):
        if current_user.is_active and current_user.is_authenticated:
            if 'admin' in current_user.roles:
                return True
            else:
                abort(403)
        else:
            return False

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login')+'?next=/admin/role')


class UserModelAdmin(ModelView):
    column_list = ('username', 'email', 'active', 'create_datetime', 'update_datetime')
    # create_modal = True

    def is_accessible(self):
        if current_user.is_active and current_user.is_authenticated:
            if 'admin' in current_user.roles:
                return True
            else:
                abort(403)
        else:
            return False

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login')+'?next=/admin/blogger')


class AuthorModelAdmin(ModelView):
    column_list = ('first_name', 'last_name', 'date_of_birth', 'date_of_death', 'books')
    # create_modal = True

    def is_accessible(self):
        if current_user.is_active and current_user.is_authenticated:
            if 'admin' in current_user.roles:
                return True
            else:
                abort(403)
        else:
            return False

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login')+'?next=/admin/blogger')


class BookModelAdmin(ModelView):
    column_list = ('title', 'isbn', 'price', 'count', 'authors')
    # create_modal = True

    def is_accessible(self):
        if current_user.is_active and current_user.is_authenticated:
            if 'admin' in current_user.roles:
                return True
            else:
                abort(403)
        else:
            return False

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login')+'?next=/admin/blogger')


class GenreModelAdmin(ModelView):
    column_list = ('name',)
    # create_modal = True

    def is_accessible(self):
        if current_user.is_active and current_user.is_authenticated:
            if 'admin' in current_user.roles:
                return True
            else:
                abort(403)
        else:
            return False

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login')+'?next=/admin/blogger')


class OrderModelAdmin(ModelView):
    column_list = ('user', 'price', 'order_date', 'paid', 'synchronized', 'books')
    # create_modal = True

    def is_accessible(self):
        if current_user.is_active and current_user.is_authenticated:
            if 'admin' in current_user.roles:
                return True
            else:
                abort(403)
        else:
            return False

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login')+'?next=/admin/blogger')