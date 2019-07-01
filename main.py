import requests
from flask import Flask, render_template, request, url_for, redirect, session
from flask_login import LoginManager, current_user, login_user
from flask_mail import Mail
from flask_mail import Message
from flask_security import Security, SQLAlchemyUserDatastore, login_required
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
            blank_list = []
            if current_user.searchphrases == blank_list:
                return redirect(url_for('process_themes'))
                return redirect(url_for('process_themes'))
            else:
                userthemes = current_user.searchphrases

                all_news = []

                for themes_ in userthemes:
                    url = 'https://newsapi.org/v2/everything?q=' + themes_.themename + '&apiKey=397dc499222b4d158971b8cb46f1fa4b'
                    content = requests.get(url)

                    data = content.json()
                    data_articles = data['articles']
                    all_news.append(data_articles)

                return render_template('news.html', all_news=all_news, data_articles=data_articles, datetime=datetime,
                                       userthemes=userthemes)

        if not current_user.is_authenticated:
            url = 'https://newsapi.org/v2/everything?q=java&apiKey=397dc499222b4d158971b8cb46f1fa4b'
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
            rememberuser = request.form.get('remember')

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

            confirmation_link = url_for('confirm', email=emailuser, _external=True)

            msg = Message('Content aggregator. Account Verification', sender='alex20k.x@gmail.com',
                          recipients=[emailuser])
            msg.body = 'Hello, ' + nameuser + '.' + 'Your confirmation link: {}'.format(confirmation_link)

            mail.send(msg)

            emailmsg = 'Account verification email has been sent to your e-mail address.'

            return render_template('welcome.html', emailmsg=emailmsg)


@login_required
@app.route('/process_themes', methods=['POST', 'GET'])
def process_themes():
    if request.method == 'GET':
        return render_template('themes.html')
    if request.method == 'POST':
        themes = {'football': request.form.get('football'),
                  'basketball': request.form.get('basketball'),
                  'hockey': request.form.get('hockey'),
                  'java': request.form.get('java'),
                  'cplus': request.form.get('c++'),
                  'php': request.form.get('php'),
                  'usa': request.form.get('usa'),
                  'russia': request.form.get('russia'),
                  'india': request.form.get('india')}

        for keys in themes:
            if themes[keys] == 'on':
                theme = Theme.query.filter(Theme.themename == keys).first()
                theme.related_user.append(current_user)
                db.session.commit()

        return redirect('/')


@login_required
@app.route('/edit_themes', methods=['POST', 'GET'])
def edit_themes():
    if request.method == 'GET':

        themes_names = []

        for t in current_user.searchphrases:
            themes_names.append(t.themename)

        return render_template('edit_themes.html', themes=themes_names)
    if request.method == 'POST':
        themes = {'football': request.form.get('football'),
                  'basketball': request.form.get('basketball'),
                  'hockey': request.form.get('hockey'),
                  'java': request.form.get('java'),
                  'cplus': request.form.get('c++'),
                  'php': request.form.get('php'),
                  'usa': request.form.get('usa'),
                  'russia': request.form.get('russia'),
                  'india': request.form.get('india')}

        print('football:', request.form.get('football'))
        print('basketball:', request.form.get('basketball'))
        print('hockey:', request.form.get('hockey'))

        print('java:', request.form.get('java'))
        print('c++:', request.form.get('c++'))
        print('php:', request.form.get('php'))

        user_themes = set()
        for userthemes in current_user.searchphrases:
            user_themes.add(userthemes.themename)

        new_themes = set()
        for keys in themes:
            if themes[keys] == 'on':
                if keys not in user_themes:
                    new_themes.add(keys)

        for newthemes in new_themes:
            theme = Theme.query.filter(Theme.themename == newthemes).first()
            theme.related_user.append(current_user)
            db.session.commit()

        for keys in themes:
            if themes[keys] is None:  # Football, Basketball, Hockey
                if keys in user_themes:
                    theme = Theme.query.filter(Theme.themename == keys).first()
                    theme.related_user.remove(current_user)
                    db.session.commit()

        return redirect('/')


@app.route('/confirm/<email>')
def confirm(email):
    email == session.get('emailuser')

    new_user = user_datastore.create_user(username=session.get('nameuser'), email=session.get('emailuser'),
                                          password=session.get('passworduser'))

    db.session.add(new_user)
    db.session.commit()

    curr_user = User.query.filter(User.email == session.get('emailuser')).first()

    login_user(curr_user, remember=True)
    return redirect('/')


if __name__ == "__main__":
    app.run()
