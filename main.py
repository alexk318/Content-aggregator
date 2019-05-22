from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore

from forms import regforms
import requests

app = Flask(__name__)

from configurationFile import ConfigClass

app.config.from_object(ConfigClass)

db = SQLAlchemy(app)

# python -m smtpd -n -c DebuggingServer localhost:8025 - Emulated mail server
mail = Mail(app)


from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

@app.route('/', methods=['GET', 'POST'])
def define_welcome():

    url = ('https://newsapi.org/v2/top-headlines?'
            'q=game of thrones&'
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

    if request.method == 'POST':
        nameuser = request.form['nameform']
        emailuser = request.form['emailform']
        passworduser = request.form['passwordform']

        msg = Message('Content aggregator. Confirm email', sender='Admin', recipients=[emailuser])
        msg.body = 'Hello,' + nameuser + '!'
        msg.html = 'There should be a link!'

        mail.send(msg)

        #new_user = user_datastore.create_user(name=nameuser, email=emailuser, password=passworduser)

        #db.session.add(new_user)
        #db.session.commit()

    return render_template('register.html', regforms=regforms)


@app.route('/signin', methods=['GET', 'POST'])
def define_login():
     pass

if __name__ == "__main__":
    app.run()
