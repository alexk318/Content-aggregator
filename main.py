from flask import render_template, request, url_for, redirect
from flask_mail import Message

from flask_login import LoginManager, current_user

from forms import regforms
from configurationFile import app, db, mail, ConfigClass
from models import User, Role
from flask_security import Security, SQLAlchemyUserDatastore

from itsdangerous import URLSafeTimedSerializer
import requests

app.config.from_object(ConfigClass)
login_manager = LoginManager(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/', methods=['GET', 'POST'])
def index_page():

    if not current_user.is_authenticated:
        url = 'https://newsapi.org/v2/top-headlines?q=steam&apiKey=397dc499222b4d158971b8cb46f1fa4b'
        content = requests.get(url)

        data = content.json()
        data_articles = data['articles']

        return render_template('welcome.html', data_articles=data_articles)

    if current_user.is_authenticated:
        url = 'https://newsapi.org/v2/top-headlines?q=space&apiKey=397dc499222b4d158971b8cb46f1fa4b'
        content = requests.get(url)

        data = content.json()
        data_articles = data['articles']
        return render_template('result.html', data_articles=data_articles)


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        nameuser = request.form['nameform']
        emailuser = request.form['emailform']
        passworduser = request.form['passwordform']

        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = s.dumps(emailuser, salt='email-confirm')

        new_user = user_datastore.create_user(name=nameuser, email=emailuser, password=passworduser, token=token,
                                              active=0)

        db.session.add(new_user)
        db.session.commit()

        confirmation_link = url_for('confirm_page', token=token, _external=True)

        #  python -m smtpd -n -c DebuggingServer localhost:8025 - Emulated mail server
        msg = Message('Content aggregator. Account Verification', sender='alex20k.x@gmail.com', recipients=[emailuser])
        msg.body = 'Hello, ' + nameuser + '.' \
                                          'Your confirmation link: {}' \
                                          ' .You have 1 hour to confirm your account'.format(confirmation_link)

        mail.send(msg)

        return render_template('emailsent.html', emailuser=emailuser)

    return render_template('signup.html', regforms=regforms)


@app.route('/confirm/<token>')
def confirm_page(token):
    specific_user = User.query.filter(User.token == token).first()
    specific_user.active = True

    db.session.commit()

    return 'Account activated'


if __name__ == "__main__":
    app.run()
