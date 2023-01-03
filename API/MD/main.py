import os
import re
import pymysql
import base64
import uuid
import io
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_jwt_extended import *
from passlib.hash import sha256_crypt
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta, timezone
from services.user import UserService



db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ACCESS_EXPIRES = timedelta(hours=1)
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/spec.json'  # Our API url (can of course be a local resource)


user_service = UserService(db_user,db_password,db_name,db_connection_name)
# data_service = DatasetService(db_user,db_password,db_name,db_connection_name)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000
app.config["JWT_SECRET_KEY"] =  str(os.environ.get("JWT_SECRET"))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Yourney api"
    },
)

app.register_blueprint(swaggerui_blueprint)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    #connect database
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                            unix_socket=unix_socket, db=db_name)

        #querying sql
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM TokenBlocklist WHERE jti = %s', (jti, ))
        token = cursor.fetchone()
    cnx.close()

    return token is not None

@app.route("/", methods=["GET"])
def hello():
    return "Hello, World This Is Yourney!"

# cek db user
@app.route('/db')
@jwt_required(refresh=False)
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
                users.append({'created_time': row[2], 'id_user': row[0], 'email': row[4], 'password': row[5], 'fullName': row[6]})
            cnx.close()
        return jsonify(users)
    else:
        return 'Invalid request'

    
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
            cursor.execute('SELECT * FROM user WHERE username = %s', (email, ))
            user = cursor.fetchone()
        cnx.close()

        if not user:
            return jsonify({'status': 'failed', 'message': 'no active user found'}),401

        if not sha256_crypt.verify(password, user[5]):
            return jsonify({'status': 'failed', 'message': 'either email or password is invalid'}),401
        
        # generate new token
        expires = timedelta(days=1)
        expires_refresh = timedelta(days=3)
        identity = {
            'id_user': user[0],
            'fullName': user[3],
            'email': user[4],
            'pekerjaan':user[6]
        }

        access_token = create_access_token(identity=identity, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=identity, expires_delta=expires_refresh)
        return jsonify(
            {
                'status': 'success',
                'access': access_token,
                'refresh': refresh_token,
                'user':{
                    'id_user': user[0],
                    'fullName': user[3],
                    'email': user[4],
                    'pekerjaan':user[6]
                }
            }
        ),201

    except Exception as e:
        return jsonify(
            {
                "message": str(e)
            }
        ),500

@app.route("/refresh", methods=["POST"])
def refresh():
    return user_service.refresh()

@app.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    now = datetime.now(timezone.utc)

    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                            unix_socket=unix_socket, db=db_name)
    with cnx.cursor() as cursor:
        cursor.execute('INSERT INTO TokenBlocklist(jti,type,created_at) VALUES (%s, %s, %s);', (jti, ttype, now))
        cnx.commit()
    cnx.close()
    return jsonify({"msg": "logout successful"})

# endpoint to verify jwt token works properly
# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
# @app.route("/protected", methods=["GET"])
# @jwt_required(refresh=False)
# def protected():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user['username']), 200

# get user profile
@app.route("/user/profile", methods=["PUT","GET"])
@jwt_required(refresh=False)
def user():
        #connect database
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                            unix_socket=unix_socket, db=db_name)
    if request.method == "GET":
        current_user = get_jwt_identity()
        id_user = current_user['id_user']

        #querying sql
        user = user_service.get_user_by_id(id_user)


        return jsonify(
            {
                'status': 'success',
                'user':{
                    'id_user': user[0],
                    'fullName': user[3],
                    'email': user[4],
                    'pekerjaan':user[6],
                    'user_pic': user[7]
                }
            }
        ),200

    elif request.method == "PUT":
        current_user = get_jwt_identity()
        data = request.get_json()
        id_user = current_user['id_user']

        if not data:
            return jsonify({
                'message':'empty required field'
            }), 400
        payload = []

        sql = 'UPDATE user SET '
        sqlupdated = []
        if 'fullName' in data:
            sqlupdated.append('fullName = %s ')
            payload.append(data['fullName'])
      
        if 'user_pic' in data:
            sqlupdated.append('user_pic = %s ')
            payload.append(data['user_pic'])
            
        if 'pekerjaan' in data:
            sqlupdated.append('pekerjaan = %s ')
            payload.append(data['pekerjaan'])

        for i in range(len(sqlupdated)):
            if i != 0:
                sql += ','
            sql+= sqlupdated[i]

        sql += 'WHERE id_user = %s;'
        payload.append(id_user)
        payload = tuple(payload)
    
        #connect database
        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)

        #querying sql
        with cnx.cursor() as cursor:
            cursor.execute(sql, payload)
            cursor.execute('SELECT id_user, full_name, email, pekerjaan, user_pic FROM user WHERE id_user=%s;',(id_user))
            cnx.commit()
            user = cursor.fetchone()
        cnx.close()

        return jsonify(
            {
                'id': user[0],
                'full_name': user[3],
                'email':user[4],
                'pekerjaan':user[6],
                'user_pic': user[7],
        }
        ), 200
    else:
        return jsonify({
            'message': 'invalid method'
        }), 400



    
 #register user + initialiazing kategori
@app.route("/register",methods=["POST", "GET"])
def register():
    try:
        request_data = request.get_json()
        email = request_data['email']
        password = request_data['password']
        fullName = request_data['fullName']
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
        # validate if email or fullName is used
        exist = user_service.check_existing_user(fullName, email)

        if exist:
            return jsonify(
                {
                    'message': 'user already exist'
                }
            ), 400

        #querying sql
        with cnx.cursor() as cursor:
            cursor.execute('INSERT INTO user (fullName, email, password, pekerjaan) VALUES (%s, %s, %s, %s, %s);', (fullName, email, Hpassword, pekerjaan))
            cnx.commit()
            result = cursor.fetchone()
        cnx.close()
        
        return jsonify(
            {
                'full_name': fullName,
                'email' : email,
                'pekerjaan':pekerjaan,
                'status' : "success"
        }
        ), 200
    except Exception as e:
        return jsonify({
            "message": str(e)
        })

@app.route('/images',methods=["POST", "GET"])
@jwt_required(refresh=False)
def upload():
    if request.method == 'POST':

        img = request.files
        if 'image' not in img:
            return jsonify({
                'message': 'image field must not empty'
            }), 400
        title = ''
        if img['image'] and allowed_file(img['image'].filename):  
            title = str(uuid.uuid4()) + secure_filename(img['image'].filename)
        else:
            return  jsonify({
                'message': 'invalid type format, allowed format (png, jpg, jpeg, gif)'
            }), 400
        encoded = base64.b64encode(img['image'].read())
        

        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)
        try:
            with cnx.cursor() as cursor:
                cursor.execute('INSERT INTO pictures(pic,title) VALUES (%s, %s);', (encoded, title))
                cnx.commit()
            cnx.close()
            return jsonify({
                'status':  'success',
                'url': request.base_url+'/'+title
            })
        except Exception as e:
            return jsonify({
                'message': str(e)
            })

@app.route('/images/<string:title>',methods=["GET"])
def get_image(title):
    if request.method == 'GET':
        if title == None:
            return({
                "message": "title need to be specified"
            }), 400

        if os.environ.get('GAE_ENV') == 'standard':
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            cnx = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name)
        try:
            with cnx.cursor() as cursor:
                cursor.execute('SELECT pic, title FROM  pictures WHERE title=%s;', (title))
                image = cursor.fetchone()
            cnx.close()
        except Exception as e:
            return jsonify({
                'message': str(e)
            }),400

        binary_data = base64.b64decode(image[0])
        return send_file(io.BytesIO(binary_data), as_attachment=True, download_name=image[1])

    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
