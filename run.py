from flask import Flask, request
from flask import make_response
from flask import request
from flask import jsonify
from naver_api import naver_api

import json
import csv
import utils

app = Flask(__name__)

eng_to_kor = {}
kor_to_eng = {}


@app.route('/')
def index():
    return "test"


## Api for CSR
@app.route('/CSR', methods=['POST'])
def speech_recognition():
    value = request
    #print(value)
    #print(value.data)

    #file = open('./test_files/csr_sample1.mp3', 'rb')
    #ret = naver_api.CSR(file)
    
    
    return "success"


## Api for CSS
@app.route('/CSS')
def speech_synthesis():
    text = "자동자 1, 마우스 2"
    ret = naver_api.CSS(text)
    
    audio_file = ret["response_content"]

    with open('./test_files/css_sample.mp3', 'wb') as f: 
        f.write(audio_file)

    return ret



## Api for OD
@app.route('/OD', methods=["POST"])
def object_detection():
    value = request

    file = value.data
    ret = naver_api.OD(file)
    
    ## if response code is not 200, then return error
    if ret["response_code"] != 200:
        return "Error code : " + ret["response_code"]

    content = eval(ret["response_content"])
    content = content['predictions'][0]
    #print(content)

    object_info = {}
    object_info["names"] = []
    object_info["positions"] = []

    # boundary for detection score
    boundary = 0.75
    
    # use only objects that are recognized by higher score than boundary
    for a in range(len(content["detection_scores"])):
        probability = content["detection_scores"][a]
        if probability >= boundary:
            object_info["names"].append(eng_to_kor[content["detection_names"][a]])
            object_info["positions"].append(content["detection_boxes"][a])
    

    # get string for client : object position representing string
    ret_string = utils.get_object_positioned_string(object_info)


    ## request text->audio conversion api
    ret = naver_api.CSS(ret_string)
    audio_file = ret["response_content"]


    # save response audio file
    #with open('./test_files/test.mp3', 'wb') as f: 
    #    f.write(audio_file)

    return ret_string


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    ## make dictionary for kor2eng, eng2kor
    with open('./mscoco.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            eng = row[0]
            kor = row[1]
            if line_count==0:
                eng = eng[1:]
            line_count += 1
            eng_to_kor[eng] = kor
            kor_to_eng[kor] = eng


    app.run(debug=True)
