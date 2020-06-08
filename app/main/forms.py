from app import db
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User , Device
from flask_wtf.file import  FileField, FileAllowed, FileRequired


class EditProfileFrom(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')
    # Avatar

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileFrom, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please  use a diffrent username.')


class UploadAvatarForm(FlaskForm):
    image = FileField('Upload', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'The file foramt should be .jpg or .png')
    ])
    submit = SubmitField()

class DeviceForm(FlaskForm):
    mac_addres = StringField('MAC:', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, mac_addres):
        device= Device.query.filter_by(mac_addres=mac_addres.data).first()
        if device is not None:
            raise ValidationError('Please use a diffrent mac_addres.')


    # def insert_person(self, mac_addres):
    #     db.session.add(mac_addres)
    #     row_count = Device.query.count()
    #     if row_count > 3:
    #         first_mac_address = User.query.order_by(Device.mac_addres.asc()).first()
    #         db.session.delete(first_mac_address)
    #     db.session.commit()
