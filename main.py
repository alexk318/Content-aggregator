from flask import render_template, request
from flask_mail import Message

from flask_security import SQLAlchemyUserDatastore

from forms import regforms
from configurationFile import app, db, mail, ConfigClass
from models import User, Role
from itsdangerous import URLSafeTimedSerializer
import requests

app.config.from_object(ConfigClass)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@app.route('/', methods=['GET', 'POST'])
def define_welcome():

    url = 'https://newsapi.org/v2/top-headlines?q=game of thrones&apiKey=397dc499222b4d158971b8cb46f1fa4b'

    content = requests.get(url)

    data = content.json()
    data_articles = data['articles']

    return render_template('welcome.html', data_articles=data_articles)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
@app.route('/signup', methods=['GET', 'POST'])
def define_register():

    if request.method == 'POST':
        nameuser = request.form['nameform']
        emailuser = request.form['emailform']
        passworduser = request.form['passwordform']

        # python -m smtpd -n -c DebuggingServer localhost:8025 - Emulated mail server
        msg = Message('Content aggregator. Confirm email', sender='Admin', recipients=[emailuser])
        msg.body = 'Hello,' + nameuser + '!'
        msg.html = 'There should be a link!'

        mail.send(msg)

        # new_user = user_datastore.create_user(name=nameuser, email=emailuser, password=passworduser)

        # db.session.add(new_user)
        # db.session.commit()

    return render_template('signup.html', regforms=regforms)


@app.route('/signin', methods=['GET', 'POST'])
def define_login():
    pass


if __name__ == "__main__":
    app.run()
