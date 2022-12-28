from flask import Flask, jsonify, Response, request
import json

app = Flask(__name__)

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

if __name__=='__main__':
    app.run(debug=True)