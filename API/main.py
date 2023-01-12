# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_cloudsql_mysql]
# [START gae_python3_cloudsql_mysql]
import os
from passlib.hash import sha256_crypt
from flask import Flask, jsonify, request
import pymysql
import re
# from services.user import UserService

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)


@app.route('/db')
def db():
    #sudah okay
    users = []
    if request.method == 'GET':
        if os.environ.get('GAE_ENV') == 'standard':
            # If deployed, use the local socket interface for accessing Cloud SQL
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM user;')
            for row in cursor:
                users.append({'created_time': row[2], 'id_user': row[0], 'email': row[5], 'password': row[6], 'pekerjaan': row[4]})
            cnx.close()
        return jsonify(users)
    else:
        return 'Invalid request'
    
    
@app.route('/getHospital')
def getHospital():
    #sudah okay
    hospital = []
    if request.method == 'GET':
        if os.environ.get('GAE_ENV') == 'standard':
            # If deployed, use the local socket interface for accessing Cloud SQL
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)
        with cnx.cursor() as cursor:
            cursor.execute('SELECT * FROM hospital;')
            for row in cursor:
                hospital.append({'id_hospital': row[0], 'image': row[6], 'name': row[1], 'address': row[2], 'region': row[3], 'phone': row[4], 'province': row[5]})
            cnx.close()
        return jsonify(hospital)
    else:
        return 'Invalid request'


#register user + initialiazing kategori
@app.route("/register",methods=["POST", "GET"])
def register():
    if request.method == 'POST':

        try:
            request_data = request.get_json()
            email = request_data['email']
            password = request_data['password']
            full_name = request_data['full_name']
            pekerjaan = request_data['pekerjaan']
            Hpassword = sha256_crypt.encrypt(password)   
            
            #connect database
            if os.environ.get('GAE_ENV') == 'standard':
                unix_socket = '/cloudsql/{}'.format(db_connection_name)
                cnx = pymysql.connect(user=db_user, password=db_password,
                                    unix_socket=unix_socket, db=db_name)
            else:
                host = '127.0.0.1'
                cnx = pymysql.connect(user=db_user, password=db_password,
                                    host=host, db=db_name)
            #validation
            # password
            if not re.fullmatch(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$', password):
                return jsonify(
                    {
                        'message': 'password character must be atleast 8 character with capital case and number charachter'
                    }
                ), 400

            # email
            emailformat = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if not re.fullmatch(emailformat, email):
                return jsonify(
                    {
                        'message': 'email is not in valid format'
                    }
                ), 400
            # # validate if email or username is used
            # exist = user_service.check_existing_user(full_name, email)

            # if exist:
            #     return jsonify(
            #         {
            #             'message': 'user already exist'
            #         }
            #     ), 400

            #querying sql
            with cnx.cursor() as cursor:
                cursor.execute('INSERT INTO user (full_name, email, password, pekerjaan) VALUES (%s, %s, %s, %s);', (full_name, email, Hpassword, pekerjaan))
                cnx.commit()
                result = cursor.fetchone()
            cnx.close()

            return jsonify({
                    "full_name": full_name,
                    "email" : email,
                    "pekerjaan" : pekerjaan,
                    "code": "sukses",
                })
        except Exception as e:
            return jsonify({
                "message": str(e)
            })
    else:
        return 'Invalid request'

#login
@app.route("/login",methods=["POST", "GET"])
def login():
    if request.method == 'POST' :
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
                return jsonify({'status': 'failed', 'message': 'either username or password is invalid'}),401
            
            return jsonify(
                {
                    'status': 'success',
                    'user':{
                        'iduser' : user[0],
                        'email': user[5],
                        'pekerjaan': user[4],
                        'full_name': user[3],
                        'user_pic': user[7],
                    }
                }
            ),201

        except Exception as e:
            return jsonify(
                {
                    "message": str(e)
                }
            ),500
    else:
        return 'Invalid request'

        


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
