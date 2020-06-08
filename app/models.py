import os
import base64
from app import db, login
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from hashlib import md5
from typing import List
from flask_serialize import FlaskSerializeMixin
from app import ma
from time import time
import jwt


FlaskSerializeMixin.db = db


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(100), index=True)
    last_name = db.Column(db.String(100),index=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    devices = db.relationship('Device', backref='owner', lazy='dynamic')
    # добавить поле  топика и мак адресаса
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)



    def __init__(self, username,email,first_name,last_name):
        self.username = username,
        self.email = email,
        self.first_name = first_name,
        self.last_name = last_name,



    def __repr__(self):
        return '<User {}'.format(self.username)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'last_seen': self.last_seen,
            'devices': self.devices,
            'avatar': self.avatar(128)
            }
        return data
    def from_dict(self, data, new_user=False):
        for field in ['username','email']:
            if field in data:
                setattr(self, field, data[field])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if  self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64decode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

class Device (db.Model, FlaskSerializeMixin):
    id = db.Column(db.Integer, primary_key=True)
    mac_addres = db.Column(db.String(80), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    position = db.relationship('Position',uselist = False, backref='device')


    # def __init__(self, mac_addres, user_id):
    #     self.mac_addres = mac_addres,
    #     self.user_id = user_id
    def __repr__(self):
        return '< MAC address {}'.format(self.mac_addres)



    def to_dict(self):
        data = {
            'id': self.id,
            'mac_address': self.mac_addres,

        }
        return data

class Position(db.Model):
    STATUS_OFFLINE = 0
    STATUS_ONLINE = 1

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    position = db.Column(db.String(30))
    status = db.Column(db.SmallInteger, default=STATUS_OFFLINE)

    def __repr__(self):
        return '< Position {}, {} , {}'.format(self.user_id, self.device, self.position)

    def dict(self):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'mac_address': self.device,
            'position': self.position,
            'satus': self.status,
        }
        return data



class DeviceSchema(ma.SQLAlchemySchema):
    mac_addres = ma.auto_field()
    class Meta:
        model = Device


class UserSchema(ma.SQLAlchemySchema):
    username = ma.auto_field()

    devices = ma.Nested(DeviceSchema, many=True)
    class Meta:
        model = User











