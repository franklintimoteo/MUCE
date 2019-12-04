from smtplib import SMTPException
import os
from threading import Thread
from flask_mail import Message
from flask import current_app, render_template
from werkzeug.urls import Href
from . import mail
from .models import get_spam, db


def send_ascync_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail_spam(email, subject, template, spam, **kwargs):
    """
    :param email: instance <Email>
    :param subject: Title Email
    :param template: directory template
    :param spam: instance <Spam>
    :param kwargs:
    :return: None
    """
    _SENDER = current_app.config['MAIL_SENDER']
    _DDNS = current_app.config['DDNS']
    template = os.path.basename(template)
    msg = Message(subject, sender=_SENDER, recipients=[email.email])
    href = Href(_DDNS)
    _url_coupon = href('/redirect', em=str(email.id), sp=str(spam.id))

    msg.html = render_template(template, url_coupon=_url_coupon, **kwargs)
    app = current_app._get_current_object()

    try:
        thr = Thread(target=send_ascync_email, args=[app, msg])
        thr.start()
    except SMTPException:
        spam.fail = spam.fail + 1

    spam.success = spam.success + 1
    db.session.add(spam)
    db.session.commit()


def send_all_emails_spam(id_spam):
    spam = get_spam(id_spam)
    for email in spam.emails:
        send_mail_spam(email, spam.title, spam.template, spam)
