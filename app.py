import os
from os.path import join, dirname
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

Mongo_client = 'mongodb+srv://test:sparta@cluster0.i8ofwto.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'
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
    msg = request.args.get('msg')
    return render_template('login.html', msg=msg)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/diskusi")
def diskusi():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('forum_diskusion.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="There was problem logging you in"))

@app.route("/sign_in", methods=["POST"])
def sign_in():
    # Sign in
    username_receive = request.form["username_give"]
    password_receive = request.form["password_give"]
    pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
    result = db.users.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": username_receive,
            # the token will be valid for 24 hours
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    # Let's also handle the case where the id and
    # password combination cannot be found
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )

@app.route('/sign_up' , methods=['POST'])
def sign_up():
    username = request.form('username')
    password = request.form('password')
    count = db.user.count_documents({})
    num = count + 1
    doc = {
        'num' :num, 
        'username' : username,
        'password' : password,
    }
    db.user.insert_one(doc)
    return jsonify({'msg': f'Account, {username} created successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
 