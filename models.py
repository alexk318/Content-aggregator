from main import db
from flask_security import UserMixin, RoleMixin

user_role_link = db.Table('user_role', db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                          db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                          )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    token = db.Column(db.String(70), unique=True)
    roles = db.relationship('Role', secondary=user_role_link, backref=db.backref('related_user', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(25), unique=True)
