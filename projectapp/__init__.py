from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from projectapp import user

from projectapp.user import userobj
from projectapp.api import apiobj

def create_app():
    app=Flask(__name__,instance_relative_config=True)
    import config
    app.config.from_object(config.LiveConfig)
    app.config.from_pyfile('config.py')
    from projectapp.mymodels import db
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'bpuser.login'
    login_manager.init_app(app)

    from .mymodels import User, Products, Category, product_category, MyModelView

    admin = Admin(app)
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Products, db.session))
    admin.add_view(MyModelView(Category, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(userobj)
    app.register_blueprint(apiobj)
    return app

from projectapp import mymodels
from projectapp import forms