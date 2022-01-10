from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

# client = MongoClient('3.38.99.10', 27017, username="test", password="test")
client = MongoClient('localhost', 27017)
db = client.hanghae99_miniproject1

@app.route('/')
def mainpage():
    return render_template('index.html')

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')
@app.route('/api/user/login')
def login():
    return render_template('login.html')
@app.route('/post_write')
def post_write():
    return render_template('post_write.html')


@app.route('/api/post/write', methods=['POST'])
def posting():
    class_title_receive = request.form['class_title_give']
    class_url_receive = request.form['class_url_give']
    class_image_receive = request.form['class_image_give']
    class_tutor_receive = request.form['class_tutor_give']
    class_desc_receive = request.form['class_desc_give']
    class_price_receive = request.form['class_price_give']

    # print("class_title_receive", class_title_receive)
    # print("class_url_receive", class_url_receive)
    # print("class_image_receive", class_image_receive)
    # print("class_tutor_receive", class_tutor_receive)
    # print("class_desc_receive", class_desc_receive)
    # print("class_price_receive", class_price_receive)

    return jsonify({"result": "success", 'msg': '포스팅 성공'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
