from flask_mail import Message
from flask import current_app, render_template
from . import mail

_SENDER = current_app.config['MAIL_SENDER']
_DDNS = current_app.config['DDNS']
def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender=_SENDER, recipients=[to])
    msg.html = render_template(template, **kwargs)
    mail.send(msg)
