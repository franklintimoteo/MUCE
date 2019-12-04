from collections.abc import MutableSequence
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .util import filter_emails
from . import login_manager


class Spam(db.Model):
    __tablename__  = 'spams'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    success = db.Column(db.Integer, nullable=True, default=0)
    fail = db.Column(db.Integer, nullable=True, default=0)
    template = db.Column(db.String, nullable=False)
    redirect_to = db.Column(db.String, nullable=True)
    captures = db.relationship('LinkCaptured', backref='spam')
    emails = db.relationship('Email', backref='spam')

    def __repr__(self):
        return "<Spam %r>" %self.title


class LinkCaptured(db.Model):
    __tablename__ = 'linkscaptured'
    id = db.Column(db.Integer, primary_key=True)
    user_agent = db.Column(db.String, nullable=True)
    ip = db.Column(db.String, nullable=True)
    os = db.Column(db.String(15), nullable=True)
    more_info = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    spam_id = db.Column(db.Integer, db.ForeignKey('spams.id'))


class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    hash = db.Column(db.String, nullable=True)
    spam_id = db.Column(db.Integer, db.ForeignKey('spams.id'))


def create_captured(usera, ip, os, more_info, email, idspam):
    captured = LinkCaptured(user_agent=usera, ip=ip, os=os, more_info=more_info, email=email, spam_id=idspam)
    db.session.add(captured)
    db.session.commit()


def _create_emails(emails):
    """
    :param emails: list emails string
    :return: Email instance db.Model
    """
    if not isinstance(emails, MutableSequence):
        raise TypeError("can only create emails with list emails")
    emails_list = []
    for email in emails:
        m = Email(email=email)
        emails_list.append(m)
    return emails_list


def create_spam_db(title, template, emails, redirect_to):
    """
    :param title: title spam
    :param template: template full path
    :param emails: list emails
    :return: id spam
    """
    emails = filter_emails(emails)
    mls = _create_emails(emails)
    spam = Spam(title=title, template=template, emails=mls, redirect_to=redirect_to)
    db.session.add_all(mls)
    db.session.add(spam)
    db.session.commit()
    return spam.id


def get_all_spams():
    """
    :return: list items spam [<Spam 'self.name'>]
    """
    return Spam.query.all()


def get_spam(idspam):
    """
    :param idspam: id spam
    :return: <Spam 'self'>
    """
    return Spam.query.get(idspam)


def get_email(idemail):
    """
    :param idemail: id email
    :return: <Email 'self'>
    """
    return Email.query.get(idemail)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' %self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


