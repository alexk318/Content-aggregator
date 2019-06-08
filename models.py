from main import db
from flask_security import UserMixin, RoleMixin

user_role_link = db.Table('user_role', db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                          db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                          )


user_pharse_link = db.Table('user_searchphrase', db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                            db.Column('phrase_id', db.Integer(), db.ForeignKey('phrase.id'))
                            )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String(70), unique=True)
    verified = db.Column(db.Boolean(), default=False)
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary=user_role_link, backref=db.backref('related_user', lazy='dynamic'))
    searchphrases = db.relationship('Phrase', secondary=user_pharse_link,
                                    backref=db.backref('related_user', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(25), unique=True)


class Phrase(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
