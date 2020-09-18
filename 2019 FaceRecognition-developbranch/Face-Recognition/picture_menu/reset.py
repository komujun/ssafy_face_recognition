import json
import requests
import os
from utility import path

def init():
    url = "https://gimic6gh9i.execute-api.ap-northeast-2.amazonaws.com/develop/faces/reset"
    json_data = {}

    json_string = json.dumps(json_data).encode("utf-8")
    response = requests.post(url, data=json_string)
    # print(response)

def remove_file():
    url = path.getDirname("pickle_data") + "/picture_pickle.pickle"
    index_url = path.getDirname("pickle_data") + "/index_pickle.pickle"
    box_url = path.getDirname("pickle_data") + "/box_pickle.pickle"
    encoding_url = path.getDirname("pickle_data") + "/encoding_pickle.pickle"

    indexE_url = path.getDirname("pickle_data") + "/indexE_pickle.pickle"
    encodings_url = path.getDirname("pickle_data") + "/encodings_pickle.pickle"

    os.remove(url)
    os.remove(index_url)
    os.remove(box_url)
    os.remove(encoding_url)
    os.remove(indexE_url)
    os.remove(encodings_url)