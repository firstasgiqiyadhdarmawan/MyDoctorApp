import os
import re
# import threading
import pymysql
import base64
import uuid
import json
import io
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_jwt_extended import *
from passlib.hash import sha256_crypt
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta, timezone
# from services.user import UserService
# from services.dataset import DatasetService

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


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
 
#login
@app.route("/login",methods=["POST", "GET"])
def login():
    try:
        request_data = request.get_json()
        email = request_data['email']
        password = request_data['password']
        #connect database
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)

        #querying sql
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM user WHERE email = %s', (email, ))
            user = cursor.fetchone()
        cnx.close()

        if not user:
            return jsonify({'status': 'failed', 'message': 'no active user found'}),401

        if not sha256_crypt.verify(password, user[6]):
            return jsonify({'status': 'failed', 'message': 'either email or password is invalid'}),401
        
        # # generate new token
        # expires = timedelta(days=1)
        # expires_refresh = timedelta(days=3)
        # identity = {
        #     'id_user': user[0],
        #     'email': user[5],
        #     'status':user[9]
        # }

        # access_token = create_access_token(identity=identity, fresh=True, expires_delta=expires)
        # refresh_token = create_refresh_token(identity=identity, expires_delta=expires_refresh)
        return jsonify(
            {
                'status': 'success',
                # 'access': access_token,
                # 'refresh': refresh_token,
                'user':{
                    'email': user[5],
                    'user_pic': user[7],
                    'fullName': user[3],
                    'pekerjaan': user[4]
                }
            }
        ),201

    except Exception as e:
        return jsonify(
            {
                "message": str(e)
            }
        ),500

           
if __name__=='__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
