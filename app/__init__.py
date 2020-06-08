from flask import Flask, request, current_app
from config import Config
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from threading import Thread, Event
from flask_login import LoginManager
from flask_avatar import Avatar
from flask_json import FlaskJSON
from flask_moment import Moment
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _l
from dotenv import load_dotenv




mqtt = Mqtt()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
moment = Moment()
socketio = SocketIO()
ma = Marshmallow()
babel = Babel()
mail = Mail()
json = FlaskJSON()
avatars = Avatar()
bootstrap = Bootstrap()
thread = Thread()
thread_stop_event = Event()
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    mqtt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    ma.init_app(app)
    babel.init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    json.init_app(app)
    thread
    thread_stop_event
    socketio.init_app(app, async_mode=None, logger=True, engineio_logger=True)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
    #if not app.debug and not app.testing:


from app import models, detection