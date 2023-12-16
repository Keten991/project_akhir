import os
from os.path import join, dirname
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

Mongo_client = ''
client = MongoClient(Mongo_client)

db = client.projectAkhir
SECRET_KEY = 'SPARTA'
TOKEN_KEY = 'mytoken'
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/diskusi")
def diskusi():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template('forum_diskusion.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="There was problem logging you in"))

# @app.route("/sign_in", methods=["POST"])
# def sign_in():
#     # Sign in
#     username_receive = request.form["username_give"]
#     password_receive = request.form["password_give"]
#     pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
#     result = db.user.find_one(
#         {
#             "id": username_receive,
#             "pw": pw_hash,
#         }
#     )
#     if result:
#         payload = {
#             "id": username_receive,
#             # the token will be valid for 24 hours
#             "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
#         }
#         token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

#         return jsonify(
#             {
#                 "result": "success",
#                 "token": token,
#             }
#         )
#     # Let's also handle the case where the id and
#     # password combination cannot be found
#     else:
#         return jsonify(
#             {
#                 "result": "fail",
#                 "msg": "We could not find a user with that id/password combination",
#             }
#         )
@app.route("/api/login", methods=["POST"])
def api_login():
    id_receive = request.form["id_give"]
    pw_receive = request.form["pw_give"]

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()
    result = db.user.find_one({"id": id_receive, "pw": pw_hash})
    if result is not None:
        payload = {
            "id": id_receive,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"result": "success", "token": token})
    else:
        return jsonify(
            {"result": "fail", "msg": "Either your email or your password is incorrect"}
        )   

@app.route('/sign_up' , methods=['POST'])
def sign_up():
    id_receive = request.form.get('id_give')
    pw_receive = request.form.get('pw_give')
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    
    verify = db.user.find_one({'id': id_receive})
    if verify:
        return jsonify({
            'result': 'fail',
            'msg': f'An account with id {id_receive} already exists. Please login!'
        })
    else:
        db.user.insert_one({
            'id': id_receive,
            'pw': pw_hash,
        })
        return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
 