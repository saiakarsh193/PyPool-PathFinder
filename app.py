from flask import Flask, render_template, jsonify, request
from pooler.pooltable import PoolTable

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/getframe', methods=['POST'])
def getFrame():
    req = request.get_json()
    pt = PoolTable(req['data'])
    pt.calculateMoves()
    resp = {'frame': pt.getFrame()}
    return jsonify(resp), 200

app.run(host='0.0.0.0', port=2501, debug=True)
