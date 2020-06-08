from flask import current_app
from threading import Thread
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subjectt, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    msg = Message(subjectt, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachments in attachments:
            msg.attach(*attachments)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
               args=(current_app._get_current_object(), msg)).start()