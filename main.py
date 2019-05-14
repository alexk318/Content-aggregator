from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from forms import regforms
import requests


app = Flask(__name__)

SECRET_KEY = 'SECRETKEY'

# mysql+driver://Name:Password@IP/DB name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:microlabm666@localhost/aggregatordb'

# Responsible for monitoring changes in the database before data is written
# to it or after data is written
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('dbcommand', MigrateCommand)

from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


@app.route('/', methods=['GET', 'POST'])
def define_welcome():

    url = ('https://newsapi.org/v2/everything?'
            'q=Football&'
            'sources=bbc-news&'
            'apiKey=397dc499222b4d158971b8cb46f1fa4b')

    try:
        content = requests.get(url)
    except requests.exceptions.ConnectionError:
        err = 'You are not connected to the Internet'
        return render_template('page.html', err=err)

    data = content.json()
    data_articles = data['articles']

    return render_template('welcome.html', data_articles=data_articles)


@app.route('/signup', methods=['GET', 'POST'])
def define_register():

    if request.methods == 'POST':
        nameuser = request.form['nameform']
        emailuser = request.form['emailform']
        passworduser = request.form['passwordform']

        new_user = user_datastore.create_user(name=nameuser, email=emailuser, password=passworduser)

        db.session.add(new_user)
        db.session.commit()

    return render_template('register.html', regforms=regforms)


@app.route('/signin', methods=['GET', 'POST'])
def define_login():
     pass

app.run(debug=True)
