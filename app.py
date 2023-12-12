import os
from os.path import join, dirname
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sign_up' , methods=['POST'])
def signip():
    username = request.form.get('username')
    password = request.form.get('password')
    doc = {
        'username' : username,
        'password' : password,
    }
    db.akun.insert_one(doc)
    return jsnotify({'result': 'succes', 'msg': f'Account, {username} created successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
 