from flask import render_template, flash, redirect, url_for, request, jsonify
from app.main import bp
from app import db
from app import ma
from app.models import User, Device, UserSchema, DeviceSchema
from werkzeug.urls import url_parse
from datetime import datetime
from app import socketio
from app import mqtt
from flask_socketio import emit

from app.main.forms import  EditProfileFrom, DeviceForm
from flask_login import current_user, login_user ,logout_user, login_required
#from app.auth.email import send_password_reset_email
from flask_json import FlaskJSON, JsonError, json_response, as_json

import flask_mqtt


@socketio.on('publish')
@bp.route('/')
@bp.route('/index')
@login_required
def index():

    users = User.query.order_by(User.username).all()
    devices = Device.query.order_by(Device.timestamp.desc(), False)
    # Топик -> Разбираеться -> Присвайваються значение

    return render_template('index.html',users=users , devices = devices, title='Home', async_mode=socketio.async_mode)

# @bp.route('/api', methods=['GET'])
# @login_required
# def apiUsers():
#     users = User.query.all()
#     user_shema = UserSchema(many=True)
#     output = user_shema.dump(users)
#     return jsonify(output)

# @bp.route('/api/devices', methods=['GET'])
# @login_required
# def apiDevices():
#     devices = Device.query.all()
#     device_schema = DeviceSchema(many=True)
#     output = device_schema.dump(devices )
#     return jsonify(output)


@socketio.on('publish')
@bp.route('/user/<username>', methods=['GET','POST'])
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()
    form = DeviceForm()
    devices = Device.query.order_by(Device.timestamp.desc(),False)



    if form.validate_on_submit():
        mac_addres = Device(mac_addres=form.mac_addres.data, owner=current_user)
        db.session.add(mac_addres)
        db.session.commit()
        flash('Your post is now live')
        # json.loads(jsonify(data={'topic': 'sensors/drone01/altitude','message': '{}'.format(form.mac_addres.data)}))
        return redirect(url_for('main.index'))

    return render_template('user.html',title='/user/<username>', user=user, form=form, devices=devices)



@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileFrom(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your Changes have been saved')
        return  redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title ='Edit Profile', form=form)

@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)







