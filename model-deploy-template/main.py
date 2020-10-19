import re
import copy
from flask import Flask
from flask import request
from flask_cors import *
import json



def model_request_handler1(kwargs):
    return kwargs


model_request_handler_store = []

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
            response['data'] = model_request_handler1(data_dict)
        except Exception as e:
            print(e)
            response['status'] = 503
        return response



if __name__ == '__main__':
    app.run()