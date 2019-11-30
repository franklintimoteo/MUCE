from . import db


class Spam(db.Model):
    __tablename__  = 'spams'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    success = db.Column(db.Integer, nullable=True)
    fail = db.Column(db.Integer, nullable=True)
    template = db.Column(db.String, nullable=False)
    captures = db.relationship('LinkCaptured', backref='spam')
    emails = db.relationship('Email', backref='spam')


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

