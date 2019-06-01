from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_mail import Message
from flask_login import LoginManager, current_user, login_user
from forms import regforms, logforms
from flask_security import Security, SQLAlchemyUserDatastore
from itsdangerous import URLSafeTimedSerializer
import requests
from werkzeug.exceptions import BadRequestKeyError

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

mail = Mail(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        url = 'https://newsapi.org/v2/top-headlines?country=ru&apiKey=397dc499222b4d158971b8cb46f1fa4b'
        content = requests.get(url)

        data = content.json()
        data_articles = data['articles']

        if request.method == 'POST':
            try:
                # Authorization forms do not have a username form, werkzeug complains about it.
                # This is how the interpreter determines if it is authorization or registration.
                nameuser = request.form['nameform']
            except BadRequestKeyError:
                emailuser = request.form['emailform']
                passworduser = request.form['passwordform']
                rememberuser = request.form['checkbox']

                specific_user = User.query.filter_by(email=emailuser).first()

                if not specific_user:
                    return render_template('welcome.html', data_articles=data_articles[:3], regforms=regforms,
                                           logforms=logforms)

                login_user(specific_user, remember=rememberuser)
            else:
                emailuser = request.form['emailform']
                passworduser = request.form['passwordform']

                s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
                token = s.dumps(emailuser, salt='email-confirm')

                confirmation_link = url_for('confirm', token=token, _external=True)

                msg = Message('Content aggregator. Account Verification', sender='alex20k.x@gmail.com',
                              recipients=[emailuser])
                msg.body = 'Hello, ' + nameuser + '.' \
                                                  'Your confirmation link: {}' \
                                                  ' .You have 1 hour to confirm your account'.format(confirmation_link)

                mail.send(msg)

                new_user = user_datastore.create_user(name=nameuser, email=emailuser, password=passworduser,
                                                      token=token)

                db.session.add(new_user)
                db.session.commit()

                return render_template('emailsent.html', emailuser=emailuser)

    if current_user.is_authenticated:
        url = 'https://newsapi.org/v2/everything?q=USA&apiKey=397dc499222b4d158971b8cb46f1fa4b'
        content = requests.get(url)

        data = content.json()
        data_articles = data['articles']

        return render_template('news.html', data_articles=data_articles)

    return render_template('welcome.html', data_articles=data_articles[:3], regforms=regforms, logforms=logforms)


@app.route('/confirm/<token>')
def confirm(token):
    specific_user = User.query.filter(User.token == token).first()
    specific_user.active = True

    db.session.commit()

    return 'Account activated'


if __name__ == "__main__":
    app.run()
