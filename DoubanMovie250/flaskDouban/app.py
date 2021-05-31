from flask import Flask,render_template,flash,request
import sqlite3


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def hello_world():
    return index()

@app.route('/movie')
def movie():
    dataList = []
    conn = sqlite3.connect('movie250.db')
    cur = conn.cursor()
    sql = "select * from movie250"
    data = cur.execute(sql)
    for item in data:
        dataList.append(item)
    cur.close()
    conn.close()
    return render_template('movie.html',movies = dataList)

@app.route('/score')
def score():
    return render_template('score.html')

@app.route('/word')
def word():
    return render_template('word.html')

@app.route('/team')
def team():
    return render_template('team.html')


if __name__ == '__main__':
    app.run(debug=True)
