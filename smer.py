from flask import Flask
from app import db
from app import mqtt
from app import socketio
from flask_socketio import emit
from app.models import User
import json
from app import current_app



app = current_app


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True, debug=True)