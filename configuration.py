from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore

app = Flask(__name__)

SECRET_KEY = 'SECRETKEY'

manager = Manager(app)
manager.add_command('dbcommand', MigrateCommand)

# mysql+driver://Name:Password@IP/DB name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:microlabm666@localhost/aggregatordb'

# Responsible for monitoring changes in the database before data is written
# to it or after data is written
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

migrate = Migrate(app, db)
