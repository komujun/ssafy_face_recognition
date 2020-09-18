import json
import requests
import os
import sys
import shutil
import urllib.request
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from utility import path, download, pickle
from picture_util import detecting, clustering, saving

def web_play():
        # =========================================
        # 이미지 다운로드

        URL1 = 'https://gimic6gh9i.execute-api.ap-northeast-2.amazonaws.com/develop/pictures/processing'
        URL2 = 'https://gimic6gh9i.execute-api.ap-northeast-2.amazonaws.com/develop/pictures/{:d}/faces'
        URL3 = 'https://gimic6gh9i.execute-api.ap-northeast-2.amazonaws.com/develop/pictures/{:d}'
        URL4 = 'https://gimic6gh9i.execute-api.ap-northeast-2.amazonaws.com/develop/noti/albums/{:d}/modified'
        URL5 = 'https://gimic6gh9i.execute-api.ap-northeast-2.amazonaws.com/develop/albums/{:d}'

        response = requests.get(URL1)
        data = download.getWebDownload(response)

        # =========================================
        # 이미지 저장
        url = path.getDirname("pickle_data") + "/picture_pickle.pickle"
        data_temp, data = saving.picture_saving(url, data)

        # print(len(data), len(data_temp))

        # =========================================
        # 재 로드 하기
        data = pickle.ReadPickle(url)
        print('pickle 로드 완료!')

        index_url = path.getDirname("pickle_data") + "/index_pickle.pickle"
        box_url = path.getDirname("pickle_data") + "/box_pickle.pickle"
        encoding_url = path.getDirname("pickle_data") + "/encoding_pickle.pickle"

        indexE_url = path.getDirname("pickle_data") + "/indexE_pickle.pickle"
        encodings_url = path.getDirname("pickle_data") + "/encodings_pickle.pickle"

        index = saving.util_saving("index", index_url)
        box = saving.util_saving("box", box_url)
        encoding = saving.util_saving("encoding", encoding_url)

        indexE = saving.util_saving("indexE", indexE_url)
        encodings = saving.util_saving("encodings", encodings_url)

        # =========================================
        # 이미지 detecting

        # data.loc[data.index == 1, 'encoding'] = 'complete'
        data_temp = data.loc[data['encoding'] == "empty"]
        result = data_temp.index

        for x in range(len(data)):
                cl_album = data.loc[data.index == x, 'album_id'].item()
                cl_picture = data.loc[data.index == x, 'picture_id'].item()
                if x in result:
                        url_path = data.loc[data.index == x, 'picture_url'].item()
                        dirname = path.getDirname("download") + "/" + data.loc[data.index == x, 'picture_name'].item()
                        urllib.request.urlretrieve(url_path, dirname)

                        box_t, encoding_t = detecting.WebfaceDetect(dirname, data.ix[x])
                        # print(box_t)
                        if len(box_t) > 0 and len(encoding_t) > 0:
                                index.append(x)
                                box.append(box_t)
                                encoding.append(encoding_t)

                                temp_len = len(index) - 1
                                for y in range(len(box[temp_len])):
                                        indexE.append(str(x) + "." + str(y))
                                        encodings.append( encoding[temp_len][y] )

                                data.loc[data.index == x, 'box'] = len(box[temp_len])
                                data.loc[data.index == x, 'encoding'] = "complete"

                                clustering.cluster(data, indexE, encodings)

                                cl_data1 = data.loc[data.index == x, 'clustering'].item()
                                cl_data2 = cl_data1.split(";")
                                cl_len = -1

                                cnt = 0
                                for top, right, bottom, left in box_t:
                                        for r in range(len(cl_data2) - 1):
                                                # print(cl_data2[r].split(".")[0])
                                                if(int(cl_data2[r].split(".")[0].strip()) == cnt):
                                                        cl_len = r
                                        
                                        # print(cl_len)
                                        json_data = {
                                                'rect_x': left,
                                                'rect_y': top,
                                                'rect_width': right - left,
                                                'rect_height': bottom - top,
                                                'cluster_id': cl_data2[cl_len].split(".")[-1]
                                        }
                                        json_string = json.dumps(json_data).encode("utf-8")
                                        post_url = URL2.format(cl_picture)
                                        print(cl_len, json_data, post_url)
                                        response = requests.post(post_url, data=json_string)
                                        cnt += 1

                        else:
                                data.loc[data.index == x, 'box'] = -1
                                data.loc[data.index == x, 'encoding'] = "Fail"
                                        
                        os.remove(dirname)

                        json_data = {
                                'status': 'checking'
                        }
                        json_string = json.dumps(json_data).encode("utf-8")
                        put_url = URL3.format(int(cl_picture))
                        # print(json_data, put_url)
                        response = requests.put(put_url, data=json_string)

                        json_data = {}
                        json_string = json.dumps(json_data).encode("utf-8")
                        post_url = URL4.format(cl_album)
                        response = requests.post(post_url, data=json_string)

        json_data = {
                'status': 'checking'
        }
        json_string = json.dumps(json_data).encode("utf-8")
        post_url = URL5.format(cl_album)
        response = requests.put(post_url, data=json_string)

        # =========================================
        # 저장하기
        pickle.WritePickle(url, data)

        pickle.WritePickle(index_url, index)
        pickle.WritePickle(box_url, box)
        pickle.WritePickle(encoding_url, encoding)

        pickle.WritePickle(indexE_url, indexE)
        pickle.WritePickle(encodings_url, encodings)
        # print(data)
        data.to_csv("test.csv", mode='w')