import os
import re
# import threading
# import pymysql
from flask_mysqldb import MySQL
import MySQLdb.cursors
import base64
import uuid
import io
import json
from flask import Flask, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
from flask_jwt_extended import *
from passlib.hash import sha256_crypt
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta, timezone
# from services.user import UserService
# from services.dataset import DatasetService

# untuk user dapat mengirimkan foto untuk profile picture
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ACCESS_EXPIRES = timedelta(hours=1)
# user_service = UserService(db_user,db_password,db_name,db_connection_name)
# data_service = DatasetService(db_user,db_password,db_name,db_connection_name)

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydoctor'
mysql = MySQL(app)

# rute test
@app.route('/', methods = ['GET'])
def hello():
    data = {"data": "Hello World"}
    return jsonify(data)

# rute untuk mendapatkan data hoax
@app.route('/getHoax', methods = ['GET'])
def getHoax():
    with open ('G:\TUGAS KULIAH\Semester 7\PemMob\MyDoctorApp\API\static\data\hoax\hoax.json', encoding='utf-8') as f:
        lines = json.loads(f.read())

    return jsonify(lines)

# rute untuk mendapatkan data hospital
@app.route('/getHospital', methods = ['GET'])
def getHospital():
    with open ('G:\TUGAS KULIAH\Semester 7\PemMob\MyDoctorApp\API\static\data\hospital\hospital.json', encoding='utf-8') as f:
        lines = json.loads(f.read())

    return jsonify(lines)

# rute untuk mendapatkan data berita mengenai covid
@app.route('/getNews', methods = ['GET'])
def getNews():
    with open ('G:\TUGAS KULIAH\Semester 7\PemMob\MyDoctorApp\API\static\data\zNews\zNews.json', encoding='utf-8') as f:
        lines = json.loads(f.read())

    return jsonify(lines)

# rute untuk mendapatkan data status
@app.route('/getStats', methods = ['GET'])
def getStats():
    with open ('G:\TUGAS KULIAH\Semester 7\PemMob\MyDoctorApp\API\static\data\stats\stats.json', encoding='utf-8') as f:
        lines = json.loads(f.read())

    return jsonify(lines)

# rute untuk login
@app.route('/login', methods=['GET','POST'])
def login():
    try:
        request_data = request.get_json()
        email = request_data['username']
        password = request_data['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email, ))
        user = cursor.fetchone()
        cursor.close()
        if not user:
            return jsonify({'status': 'failed', 'message': 'no active user found'}),401 
         
        if not sha256_crypt.verify(password, user[5]):
            return jsonify({'status': 'failed', 'message': 'either email or password is invalid'}),401    
        
        return jsonify (
            {
                "status" : "Success",
                "user" :{
                    "email" : user[4],
                    "Full Name" : user[3]
                }
            }
        ),201
    
    except Exception as e:
        return jsonify (
            {
                "msg" : str(e)
            }
        ),500
           
if __name__=='__main__':
    app.run(debug=True)