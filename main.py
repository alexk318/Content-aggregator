import requests
from flask import Flask, render_template, request, url_for, redirect, session
from flask_login import LoginManager, current_user, login_user
from flask_mail import Mail
from flask_mail import Message
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from werkzeug.exceptions import BadRequestKeyError
from datetime import datetime

from forms import regforms, logforms, theforms

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

mail = Mail(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

from models import User, Role, Theme

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('news.html')

        if not current_user.is_authenticated:
            url = 'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=397dc499222b4d158971b8cb46f1fa4b'
            content = requests.get(url)

            data = content.json()
            data_articles = data['articles']

            return render_template('welcome.html', data_articles=data_articles[:3], regforms=regforms,
                                   logforms=logforms, theforms=theforms, datetime=datetime)

    if request.method == 'POST':
        try:
            # Authorization forms do not have a username form, werkzeug complains about it.
            # This is how the interpreter determines if it is authorization or registration.
            nameuser = request.form['nameform']
        except BadRequestKeyError:  # Authorization
            emailuser = request.form['emailform']
            passworduser = request.form['passwordform']
            rememberuser = True if request.form['checkbox'] else False

            specific_user = User.query.filter_by(email=emailuser).first()

            if not specific_user:
                return redirect('/')

            login_user(specific_user, remember=rememberuser)
            return redirect('/')

        else:  # Registration
            emailuser = request.form['emailform']
            passworduser = request.form['passwordform']

            s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            token = s.dumps(emailuser, salt=app.config['SECURITY_PASSWORD_SALT'])

            session['nameuser'] = nameuser
            session['emailuser'] = emailuser
            session['passworduser'] = passworduser
            session['r_phrase'] = r_phrase
            session['b_phrase'] = b_phrase
            # session['token'] = token

            confirmation_link = url_for('confirm', email=emailuser, _external=True)

            msg = Message('Content aggregator. Account Verification', sender='alex20k.x@gmail.com',
                          recipients=[emailuser])
            msg.body = 'Hello, ' + nameuser + '.' + 'Your confirmation link: {}'.format(confirmation_link)

            mail.send(msg)

            emailmsg = 'Account verification email has been sent to your e-mail address.'

            return render_template('welcome.html', emailmsg=emailmsg)


@app.route('/confirm/<email>')
def confirm(email):
    email == session.get('emailuser')

    new_user = user_datastore.create_user(name=session.get('nameuser'), email=session.get('emailuser'),
                                          password=session.get('passworduser'))

    db.session.add(new_user)
    db.session.commit()

    curr_user = User.query.filter(User.email == session.get('emailuser')).first()

    themes = {'Real Madrid': session.get('r_phrase'), 'Barcelona': session.get('b_phrase')}

    for keys in themes:
        if themes[keys] is True:
            phrase = Theme.query.filter(Theme.themename == keys).first()
            phrase.related_user.append(curr_user)
            db.session.commit()

    login_user(curr_user, remember=True)
    return redirect('/')


if __name__ == "__main__":
    app.run()
