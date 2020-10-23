import re
import copy
from flask import Flask, request
from flask_cors import *
import json


def preprocess(data_slice):
    for i in range(len(data_slice)):
        data_slice[i] = [data_slice[i][0], data_slice[i][2], data_slice[i][3], data_slice[i][1]]
    return data_slice

def model_core():
    pass

def model_handler(kwargs):
    datas = kwargs['data']['processedData']
    res = dict()
    res['text'] = ""
    res['source_files'] = ['ann', 'txt']
    res['annotation'] = []
    res['entities'] = []
    idx = 1
    for data in datas:
        sentence = data['sentence'][0]
        annotations = data['annotation']
        annotations = preprocess(annotations)
        single_res = dict()
        for annotation in annotations:
            single_res['{}-{}'.format(annotation[1], annotation[2])] = (annotation[3], 0.9)
        res['annotation'].append(single_res)
        for key, value in single_res.items():
            res['entities'].append(["T{}".format(idx), value[0], [[int(key.split('-')[0]) + len(res['text']), int(key.split('-')[1]) + len(res['text'])]]])
            idx += 1
        res['text'] += sentence
    
    return res

app = Flask(__name__)

CORS(app, supports_credentials=True)

@app.route('/api/model/', methods=['POST'])
def similar():
    if request.method == 'POST':
        data = request.get_data(as_text=False)
        data_dict = json.loads(data)
        response = dict()
        response['status'] = 200
        try:
            response['data'] = model_handler(data_dict)
        except Exception as e:
            print(e)
            response['status'] = 503
        return response



if __name__ == '__main__':
    app.run()