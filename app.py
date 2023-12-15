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
 