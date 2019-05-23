from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)


class ConfigClass(object):

    DEBUG = True

    SECRET_KEY = 'SECRETKEY'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:microlabm666@localhost/onlinestoredb'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'alex20k.x@gmail.com'
    app.config['MAIL_PASSWORD'] = 'jetP1102'


mail = Mail()
mail.init_app(app)

db = SQLAlchemy(app)
