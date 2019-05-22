from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
mail = Mail(app)


class ConfigClass(object):

    DEBUG = True

    # Automatic reload of the site when adding new changes to the code
    SECRET_KEY = 'SECRETKEY'

    # mysql+driver://Name:Password@IP/DB name
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:microlabm666@localhost/onlinestoredb'

    # Responsible for monitoring changes in the database before data is written
    # to it or after data is written
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
