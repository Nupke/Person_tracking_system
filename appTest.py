from flask import Flask
from app import db
from app.models import User ,Device
from app import socketio

app = Flask(__name__)
app.config['SECRET_KEY']  = '19960208'


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True, debug=True)