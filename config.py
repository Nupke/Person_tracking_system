import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'savehome'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://andrey:@localhost/andrey'
    DEBUG = True

    MQTT_BROKER_URL = '127.0.0.1'
    MQTT_BROKER_PORT = 1883
    MQTT_CLIENT_ID = 'flask-mqtt'
    MQTT_USERNAME = ''
    MQTT_PASSWORD = ''
    MQTT_KEEPALIVE = 5
    MQTT_TLS_ENABLED = False
    MQTT_LAST_WILL_TOPIC = 'sensors/drone01/altitude'
    MQTT_LAST_WILL_MESSAGE = 'bye'
    MQTT_LAST_WILL_QOS = 2

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('465') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('')
    MAIL_PASSWORD = os.environ.get('')
    ADMINS = ['']
   #AVATAR
    AVATARS_SAVE_PATH = os.path.join(basedir, 'avatarts')








