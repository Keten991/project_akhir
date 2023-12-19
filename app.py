import os
from os.path import join, dirname
from pymongo import MongoClient
import requests
import jwt
from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

Mongo_client = 'mongodb+srv://test:sparta@cluster0.i8ofwto.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(Mongo_client)

db = client.projectAkhir
SECRET_KEY = 'SPARTA'
TOKEN_KEY = 'mytoken'
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/article')
def article():
    return render_template('article.html')

@app.route('/tentang_kita')
def tentang_kita():
    return render_template('tentang_kita.html')

@app.route('/artikel/detail')
def detail_artikel():
    return render_template('detail_article.html')

@app.route('/article_admin')
def article_admin():
    return render_template('article_admin.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

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
def api_signup():
    id_receive = request.form.get('id_give')
    pw_receive = request.form.get('pw_give')
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    
    verify = db.user.find_one({'id': id_receive})
    if verify:
        return jsonify({
            'result': 'fail',
            'msg': f'An account with id {id_receive} already exists. Please login!',
        })
    else:
        db.user.insert_one({
            'id': id_receive,
            'pw': pw_hash,
        })
        return jsonify({'result': 'success'})
    
@app.route('/home_article')
def home_article():
   articles = list(db.article.find({},{'_id':False}).limit(3))
   return  jsonify({'articles':articles})

@app.route('/laman_article')
def laman_article():
   articles = list(db.article.find({},{'_id':False}))
   return  jsonify({'articles':articles})

@app.route('/article',methods=['POST'])
def save_article():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    file = request.files['file_give']
    extention = file.filename.split('.')[-1]
    filename = f'static/post-articles-{extention}'
    file.save(filename)

    doc = {
        'file': filename,
        'title':title_receive,
        'content':content_receive,
    }

    db.article.insert_one(doc)
    return jsonify ({'massage':'data was saved!!!'})

@app.route('/article/<article_id>')
def article_detail(article_id):
    user_info = db.article.find_one(
            {'title': article_id},
            {'_id': False}
            )
    definitions = user_info.json()
    return render_template('detail_article.html', article=article_id, definitions=definitions)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
 