from flask import render_template, request

from forms import regforms
import requests

from configuration import app, SECRET_KEY, db, user_datastore


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

    if request.method == 'POST':
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
