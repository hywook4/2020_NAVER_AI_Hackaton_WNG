from flask import Flask
from flask import make_response
from flask import request
from flask import jsonify
from naver_api import naver_api

app = Flask(__name__)

@app.route('/')
def index():
    return "test"


@app.route('/CSR')
def speech_recognition():


    return "CSR"


@app.route('/CSS')
def speech_synthesis():
    return "CSS"


@app.route('/OD')
def object_detection():
    file = open('./test_files/od_sample1.jpeg', 'rb')
    ret = naver_api.OD(file)
    print(ret)
    return ret["response_content"]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)


data = {
    file: 'aiejflsdfsdlfskafsnlkvnsklvssafiwef',
    classification: 1 # 1 or 2
}