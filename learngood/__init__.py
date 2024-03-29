import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from flask_login import LoginManager

from flask_mail import Mail, Message

from dotenv import load_dotenv
load_dotenv()

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)


    app.config['MAIL_SERVER']='smtp.cloudmta.net'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    mail.init_app(app)
    
    app.config['SECRET_KEY'] = os.getenv("SECRETKEY")
    # url = URL.create(
    #     drivername="postgresql",
    #     username=os.getenv("USER"),
    #     password=os.getenv("PASSWORD"),
    #     host="localhost",
    #     database="mydb"
    # )

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    #app.config['SQLALCHEMY_DATABASE_URI'] = url

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from . import models

    with app.app_context():
        db.create_all()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
