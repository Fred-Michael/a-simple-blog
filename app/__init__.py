from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_class=Config):
   app = Flask(__name__)
   app.config.from_object(config_class)

   db.init_app(app)
   migrate.init_app(app, db)
   login.init_app(app)
   bootstrap.init_app(app)
   moment.init_app(app)

   from app.auth import bp as auth_bp
   app.register_blueprint(auth_bp)

   from app.main import bp as main_bp
   app.register_blueprint(main_bp)

   return app


from app import models