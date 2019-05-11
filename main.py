from flask import Flask, render_template, request
from wtforms import Form, StringField
import requests

app = Flask(__name__)

class Topic(Form):
    topicInput = StringField('Enter topic:')

topicform = Topic()

@app.route('/', methods=['GET', 'POST'])
def define_page():
    if request.method == 'POST':
        userTopic = request.form['topicInput']

        url = ('https://newsapi.org/v2/everything?'
                'q='+userTopic+'&'
                'sources=lenta&'
                'apiKey=397dc499222b4d158971b8cb46f1fa4b')

        try:
            content = requests.get(url)
        except requests.exceptions.ConnectionError:
            err = 'You are not connected to the Internet'
            return render_template('page.html', err=err)

        data = content.json()
        data_articles = data['articles']

        return render_template('result.html', data_articles=data_articles)

    return render_template('page.html', topicform=topicform)

# title
# description
# urlToImage
# publishedAt
# url

app.run(debug=True)
