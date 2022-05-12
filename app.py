from flask import Flask, render_template, jsonify, request
from pooler.pooltable import PoolTable

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/getpaths', methods=['POST'])
def getPaths():
    req = request.get_json()
    pt = PoolTable(req['frame_data'])
    pt.calculatePaths()
    resp = {'paths': pt.getPaths()}
    return jsonify(resp), 200

@app.route('/getlines', methods=['POST'])
def getLines():
    req = request.get_json()
    pt = PoolTable(req['frame_data'])
    pt.calculatePaths()
    resp = {'lines': pt.getLines()}
    return jsonify(resp), 200

app.run(host='0.0.0.0', port=2501, debug=True)
