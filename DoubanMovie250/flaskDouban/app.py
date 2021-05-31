from flask import Flask,render_template,flash,request
import sqlite3
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index .html')


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
    score =[]
    num = []
    conn = sqlite3.connect('movie250.db')
    cur = conn.cursor()
    sql = "select score,count(score) from movie250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(item[0])
        num.append(item[1])
    cur.close()
    conn.close()
    return render_template('score.html',score=score,num=num)

@app.route('/word')
def word():
    return render_template('word.html')

@app.route('/team')
def team():
    return render_template('team.html')


if __name__ == '__main__':
    app.run(debug=True)
