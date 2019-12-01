from . import db
from .util import filter_emails
from collections.abc import MutableSequence

class Spam(db.Model):
    __tablename__  = 'spams'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    success = db.Column(db.Integer, nullable=True, default=0)
    fail = db.Column(db.Integer, nullable=True, default=0)
    template = db.Column(db.String, nullable=False)
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
    spam_id = db.Column(db.Integer, db.ForeignKey('spams.id'))


class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    hash = db.Column(db.String, nullable=True)
    spam_id = db.Column(db.Integer, db.ForeignKey('spams.id'))

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

def create_spam_db(title, template, emails):
    """
    :param title: title spam
    :param template: template full path
    :param emails: list emails
    """
    emails = filter_emails(emails)
    mls = _create_emails(emails)
    spam = Spam(title=title, template=template, emails=mls)
    db.session.add_all(mls)
    db.session.add(spam)
    db.session.commit()


def get_all_spams():
    """
    :return: list items spam [<Spam 'self.name'>]
    """
    return Spam.query.all()

