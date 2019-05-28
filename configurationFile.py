from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)


SECRET_KEY = 'SECRETKEY'

SECURITY_PASSWORD_SALT = 'email-confirm'
SECURITY_PASSWORD_HASH = 'sha512_crypt'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:microlabm666@localhost/aggregatordb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'alex20k.x@gmail.com'
MAIL_PASSWORD = 'jetP1102'


mail = Mail()
mail.init_app(app)

db = SQLAlchemy(app)
