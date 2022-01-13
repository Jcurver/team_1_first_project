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

client = MongoClient('3.38.99.10', 27017, username="test", password="test")
# client = MongoClient('localhost', 27017)
db = client.db_hanghae99_miniproject1


@app.route('/')
def mainpage():
    # 메인페이지 랜더링
    mytoken = request.cookies.get('mytoken')
    # 토큰이 있는 경우 (로그인 된 경우)
    if (mytoken):
        login_status = True
        print("로그인 상태", "login_status", login_status)
    else:
        login_status = False
        print("로그인 상태", "login_status", login_status)
    return render_template('index.html', login_status=login_status)


# 1/12일 추가 -Jhmael
# 카드 리스트 불러오기
@app.route('/home', methods=['GET'])
def listing():
    token_receive = request.cookies.get('mytoken')
    print('token', token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 전체 카드 리스트 찾기
        classes = list(db.classes.find({}))
        # Id값을 string으로 변환
        for post in classes:
            post["_id"] = str(post["_id"])
            post["count_heart"] = db.likes.count_documents({"post_id": post["_id"], "type": "heart"})
            post["heart_by_me"] = bool(
                db.likes.find_one({"post_id": post["_id"], "type": "heart", "username": payload['username']}))
            post["bookmark_by_me"] = bool(
                db.bookmarks.find_one({"post_id": post["_id"], "type": "bookmark", "username": payload['username']}))
        # json값을 html에 전달
        return jsonify({'result': 'success', 'msg': '성공!', 'classes': classes})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        classes = list(db.classes.find({}))
        print(classes)
        for post in classes:
            post["_id"] = str(post["_id"])
            post["count_heart"] = db.likes.count_documents({"post_id": post["_id"], "type": "heart"})
        return jsonify({'result': 'success', 'msg': '성공!', 'classes': classes})
        # return redirect(url_for("home"))


@app.route('/mypage')
def mypage():
    mytoken = request.cookies.get('mytoken')
    # 토큰이 있는 경우 (로그인 된 경우)
    if (mytoken):
        login_status = True
        print("로그인 상태", "login_status", login_status)
        payload = jwt.decode(mytoken, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['username']})
        return render_template('mypage.html', login_status=login_status, user_info=user_info)
    else:
        login_status = False
        print("로그인 상태", "login_status", login_status)
        return render_template('mypage.html', login_status=login_status)


@app.route('/mypage/<username>/upload', methods=['GET'])
def myUpload(username):
    token_receive = request.cookies.get('mytoken')
    print('token', token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 전체 카드 리스트 찾기
        classes = list(db.classes.find({'post_writer': username}))
        # Id값을 string으로 변환
        for post in classes:
            post["_id"] = str(post["_id"])
            post["count_heart"] = db.likes.count_documents({"post_id": post["_id"], "type": "heart"})
            post["heart_by_me"] = bool(
                db.likes.find_one({"post_id": post["_id"], "type": "heart", "username": payload['username']}))
            post["bookmark_by_me"] = bool(
                db.bookmarks.find_one({"post_id": post["_id"], "type": "bookmark", "username": payload['username']}))
        # json값을 html에 전달
        return jsonify({'result': 'success', 'msg': '성공!', 'classes': classes})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/mypage/<username>/bookmark', methods=['GET'])
def myBookmark(username):
    token_receive = request.cookies.get('mytoken')
    print('token', token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 전체 카드 리스트 찾기
        classes = list(db.classes.find({}))
        # Id값을 string으로 변환
        for post in classes:
            post["_id"] = str(post["_id"])
            post["count_heart"] = db.likes.count_documents({"post_id": post["_id"], "type": "heart"})
            post["heart_by_me"] = bool(
                db.likes.find_one({"post_id": post["_id"], "type": "heart", "username": payload['username']}))
            post["bookmark_by_me"] = bool(
                db.bookmarks.find_one({"post_id": post["_id"], "type": "bookmark", "username": payload['username']}))
        # json값을 html에 전달
        return jsonify({'result': 'success', 'msg': '성공!', 'classes': classes})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# 1ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@app.route('/login')
def login_page():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# @app.route('/signup')
# def signup_page():
#     return render_template('register.html')


@app.route('/signup')
def signup_page():
    return render_template('register.html')


@app.route('/api/user/signup', methods=['POST'])
def signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.users.insert_one({'username': id_receive, 'password': pw_hash})

    return jsonify({'result': 'success'})


# 아이디 중복 여부 확인
@app.route('/api/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({'username': username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/user/login', methods=['POST'])
def login():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'username': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.users.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


# 2ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


@app.route('/post_write')
def post_write():
    return render_template('post_write.html')


@app.route('/api/post/write', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')

    if token_receive:
        print("토큰 있음")
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'username': payload['username']})

        class_title_receive = request.form['class_title_give']
        class_url_receive = request.form['class_url_give']
        class_image_receive = request.form['class_image_give']
        class_tutor_receive = request.form['class_tutor_give']
        class_desc_receive = request.form['class_desc_give']
        class_price_receive = request.form['class_price_give']

        doc = {
            "post_writer": user_info["username"],
            "class_title": class_title_receive,
            "class_url": class_url_receive,
            "class_image": class_image_receive,
            "class_instructor": class_tutor_receive,
            "class_desc": class_desc_receive,
            "class_price": class_price_receive,
        }
        db.classes.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    else:
        print("토큰 없음")
        return jsonify({"result": "failure", 'msg': '토큰 없음'})


# jhmael-----------------------------------

# [검색 API]
@app.route('/search', methods=['GET'])
def search_result():
    # token 가져오기
    token_receive = request.cookies.get('mytoken')
    if token_receive:
        login_status = True
        print("로그인 상태", "login_status", login_status)
    else:
        login_status = False
        print("로그인 상태", "login_status", login_status)
    try:
        if token_receive:
            print('found token', token_receive)
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.users.find_one({"username": payload["username"]})
            print(user_info)
            # 검색어 가져오기
            search_receive = request.args.get('search_give')

            # 검색어에 맞는 클래스 데이터 리스트 찾기
            # 검색어에 값이 있을때
            if search_receive:
                result = list(db.classes.find({'class_title': {'$regex': search_receive, '$options': 'i'}}))
                print(result)
                # classes = list(db.classes.find({}))
                for post in result:
                    # post["_id"] = str(post["_id"])
                    post["count_heart"] = db.likes.count_documents({"post_id": '_id', "type": "heart"})
                    print('카운트', post["count_heart"])
                    post["heart_by_me"] = bool(
                        db.likes.find_one({"post_id": '_id', "type": "heart", "username": payload['username']}))
                    post["bookmark_by_me"] = bool(
                        db.bookmarks.find_one({"post_id": '_id', "type": "bookmark", "username": payload['username']}))
            # 검색어가 빈값일때
            elif not search_receive:
                result = list(db.classes.find({'class_title': search_receive}))
            # 리턴
            return render_template('search.html', result=result, search_receive=search_receive,
                                   login_status=login_status)
        else:
            search_receive = request.args.get('search_give')

            # 검색어에 맞는 클래스 데이터 리스트 찾기
            # 검색어에 값이 있을때
            if search_receive:
                result = list(db.classes.find({'class_title': {'$regex': search_receive, '$options': 'i'}}))
                print(result)
                # classes = list(db.classes.find({}))
                for post in result:
                    # post["_id"] = str(post["_id"])
                    post["count_heart"] = db.likes.count_documents({"post_id": '_id', "type": "heart"})
                    print('카운트', post["count_heart"])
            # 검색어가 빈값일때
            elif not search_receive:
                result = list(db.classes.find({'class_title': search_receive}))
            # 리턴
            return render_template('search.html', result=result, search_receive=search_receive)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('/')


# [좋아요 API]
@app.route('/api/post/like', methods=['POST'])
def likes():
    token_receive = request.cookies.get('mytoken')
    try:
        if token_receive:
            print('found token', token_receive)
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.users.find_one({"username": payload["username"]})
            print('user_info', user_info)
            post_id_receive = request.form["post_id_give"]
            type_receive = request.form["type_give"]
            action_receive = request.form["action_give"]
            doc = {
                "post_id": post_id_receive,
                "username": user_info["username"],
                "type": type_receive
            }
            if action_receive == "like":
                db.likes.insert_one(doc)
            else:
                db.likes.delete_one(doc)
            count = db.likes.count_documents({"post_id": post_id_receive, "type": type_receive})
            return jsonify({"result": "success", 'msg': 'updated', "count": count})
            # 좋아요 수 변경
            # return jsonify({"result": "success", 'msg': 'updated'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))


@app.route('/api/post/bookmark', methods=['POST'])
# [북마크 API]
def bookmarks():
    token_receive = request.cookies.get('mytoken')
    try:
        if token_receive:
            print('found token', token_receive)
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = db.users.find_one({"username": payload["username"]})
            print('user_info', user_info)
            post_id_receive = request.form["post_id_give"]
            type_receive = request.form["type_give"]
            action_receive = request.form["action_give"]
            doc = {
                "post_id": post_id_receive,
                "username": user_info["username"],
                "type": type_receive
            }
            if action_receive == "bookmark":
                db.bookmarks.insert_one(doc)
            else:
                db.bookmarks.delete_one(doc)
            count = db.bookmarks.count_documents({"post_id": post_id_receive, "type": type_receive})
            return jsonify({"result": "success", 'msg': 'updated', "count": count})
            # 좋아요 수 변경
            # return jsonify({"result": "success", 'msg': 'updated'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
