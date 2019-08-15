import mysql.connector
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'SECRETKEY'

SECURITY_PASSWORD_SALT = 'email-confirm'
SECURITY_PASSWORD_HASH = 'sha512_crypt'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:microlabm666@localhost/aggregatordb'
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'x'
MAIL_PASSWORD = 'x'

del os
