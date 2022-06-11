from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'I am Ironman'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # this is to register the different .py files to the website.
    from .views import views
    from .auth import auth
    from .fibon import fibon
    from .changemachine import changemachine
    from .mortgage import mortgage
    from .mathquiz import mathquiz
    from .test import test

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(fibon, url_prefix='/')
    app.register_blueprint(changemachine, url_prefix='/')
    app.register_blueprint(mortgage, url_prefix='/')
    app.register_blueprint(mathquiz, url_prefix='/')
    app.register_blueprint(test, url_prefix='/')
    
    from .models import User, Note
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database.')