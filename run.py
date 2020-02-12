from flask import Flask
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
    file = open('./test_files/csr_sample1.mp3', 'rb')
    ret = naver_api.CSR(file)
    
    
    print(ret)
    return ret


## Api for CSS
@app.route('/CSS')
def speech_synthesis():
    text = "안녕하세요 저는 미진이 입니다"
    ret = naver_api.CSS(text)
    
    audio_file = ret["response_content"]

    with open('./test_files/css_sample.mp3', 'wb') as f: 
        f.write(audio_file)

    return ret



## Api for OD
@app.route('/OD')
def object_detection():
    file = open('./test_files/od_sample1.jpeg', 'rb')
    ret = naver_api.OD(file)
    

    if ret["response_code"] != 200:
        return "Error code : " + ret["response_code"]

    content = eval(ret["response_content"])
    content = content['predictions'][0]
    print(content)

    object_info = {}
    object_info["names"] = []
    object_info["positions"] = []

    for a in range(len(content["detection_scores"])):
        probability = content["detection_scores"][a]
        if probability >= 0.75:
            object_info["names"].append(eng_to_kor[content["detection_names"][a]])
            object_info["positions"].append(content["detection_boxes"][a])
    

    ## 0:left, 1:middle, 2:right
    pos_idx = []
    for a in range(3):
        pos_idx.append([])

    idx = 0
    left = [0, 0, 1, 0.3333]
    middle = [0, 0.3333, 1, 0.6666]
    right = [0, 0.6666, 1, 1]
    for l in object_info["positions"]:
        max_area = 0
        cur_area = 0
        chosen_idx = 0
        ## check left 
        cur_area = utils.get_intersection_area(l, left)
        if cur_area > max_area:
            max_area = cur_area
            chosen_idx = 0

        ## check middle
        cur_area = utils.get_intersection_area(l, middle)
        if cur_area > max_area:
            max_area = cur_area
            chosen_idx = 1

        ## check right
        cur_area = utils.get_intersection_area(l, right)
        if cur_area > max_area:
            max_area = cur_area
            chosen_idx = 2

        if max_area <= 0.75:
            pos_idx[chosen_idx].append(idx)

        idx += 1

        ret_string = ""

        ret_string = "왼쪽에"
        for a in pos_idx[0]:
            ret_string +=  " " + object_info["names"][a]
        ret_string += ". "

        ret_string += "중간에"
        for a in pos_idx[1]:
            ret_string += " " + object_info["names"][a]
        ret_string += ". "
    
        ret_string += "오른쪽에"
        for a in pos_idx[2]:
            ret_string += " " + object_info["names"][a]
        ret_string += "가 있습니다."
        
    ret = naver_api.CSS(ret_string)
    audio_file = ret["response_content"]

    with open('./test_files/test_subeom.mp3', 'wb') as f: 
        f.write(audio_file)


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
