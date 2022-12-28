import os
import re
# import threading
import pymysql
import base64
import uuid
import io
import json
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_jwt_extended import *
from passlib.hash import sha256_crypt
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta, timezone
from services.user import UserService
from services.dataset import DatasetService
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ACCESS_EXPIRES = timedelta(hours=1)
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/spec.json'  # Our API url (can of course be a local resource)

db_user = root
db_password =
db_name = mydoctor
db_connection_name = 127.0.0.1
user_service = UserService(db_user,db_password,db_name,db_connection_name)
data_service = DatasetService(db_user,db_password,db_name,db_connection_name)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000
app.config["JWT_SECRET_KEY"] =  str(os.environ.get("JWT_SECRET"))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

@app.route('/', methods = ['GET'])
def hello():
    data = {"data": "Hello World"}
    return jsonify(data)

@app.route('/getHoax', methods = ['GET'])
def getHoax():
    with open ('.\static\data\hoax\hoax.json', encoding='utf-8') as f:
        lines = json.loads(f.read())

    return jsonify(lines)

@app.route('/getHospital', methods = ['GET'])
def getHospital():
    with open ('.\static\data\hospital\hospital.json', encoding='utf-8') as f:
        lines = json.loads(f.read())

    return jsonify(lines)

@app.route('/getNews', methods = ['GET'])
def getNews():
    with open ('.static\data\zNews\zNews.json', encoding='utf-8') as f:
        lines = json.loads(f.read())

    return jsonify(lines)

@app.route('/getStats', methods = ['GET'])
def getStats():
    with open ('G:\TUGAS KULIAH\Semester 7\PemMob\MyDoctorApp\API\static\data\stats\stats.json', encoding='utf-8') as f:
        lines = json.loads(f.read())

    return jsonify(lines)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    #connect database 
    #TODO

        #querying sql db
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM TokenBlocklist WHERE jti = %s', (jti, ))
        token = cursor.fetchone()
    cnx.close()

    return token is not None     

@app.route("/refresh", methods=["POST"])
def refresh():
    return user_service.refresh()
           
           
           
           
           
if __name__=='__main__':
    app.run(debug=True)