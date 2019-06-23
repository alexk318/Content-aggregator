from main import db
from flask_security import UserMixin, RoleMixin

user_role_link = db.Table('user_role', db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                          db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                          )

user_theme_link = db.Table('user_theme', db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                           db.Column('theme_id', db.Integer(), db.ForeignKey('theme.id'))
                           )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary=user_role_link, backref=db.backref('related_user', lazy='dynamic'))
    searchphrases = db.relationship('Theme', secondary=user_theme_link,
                                    backref=db.backref('related_user', lazy='dynamic'))

    def __repr__(self):
        return '<{}>'.format(self.username)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(25), unique=True)


class Theme(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    themename = db.Column(db.String(100))

    def __repr__(self):
        return '<{}>'.format(self.themename)
