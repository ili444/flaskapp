from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import Security, SQLAlchemyUserDatastore, current_user

from flask import redirect, url_for, request

app = Flask(__name__) #иницилизируем приложение Flask
app.config.from_object(Configuration) #добавляем модуль с настройками



db = SQLAlchemy(app) #иницилизируем базу данных

migrate = Migrate(app, db) # иницилизируем миграции
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models import *

"""Admin"""

class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)

class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass

class BookAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'annotation', 'authors','year']

class AuthorAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'books']


admin = Admin(app, name="Flaskapp", url='/', index_view=HomeAdminView(name='Home'))

admin.add_view(BookAdminView(Books, db.session, name='Library', endpoint='library'))
admin.add_view(AuthorAdminView(Author, db.session, name='Authors', endpoint='writers'))

admin.add_view(AdminView(User, db.session, name='Users', endpoint='users'))
admin.add_view(AdminView(Role, db.session, name='Roles', endpoint='roles'))

"""User Flask-security"""

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
