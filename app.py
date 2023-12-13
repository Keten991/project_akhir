import os
from os.path import join, dirname
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

client = MongoClient('mongodb+srv://test:sparta@cluster0.z9fd051.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

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
 