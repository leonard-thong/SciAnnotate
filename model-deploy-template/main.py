import re
import copy
from flask import Flask
from flask import request
import json


app = Flask(__name__)
@app.route('/api/model/', methods=['POST'])
def similar():
    if request.method == 'POST':
        data = request.get_data(as_text=False)
        print(data)
        data_dict = json.loads(data)
        response = dict()
        # if data_dict[0]['value'] != 'axwPgdZYLjyt9cej6ED3VPKN':
        #     response['status'] = 403
        #     response['message'] = '密钥错误'
        #     return json.dumps(response)
        print(data_dict)
        return data_dict



if __name__ == '__main__':
    app.run()