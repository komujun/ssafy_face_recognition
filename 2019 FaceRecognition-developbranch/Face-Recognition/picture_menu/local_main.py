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

def local_play():
    # =========================================
    # 이미지 다운로드
    url = path.getDirname("image")
    data = download.getLinkDownload(url)

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
        if x in result:
            box_t, encoding_t = detecting.faceDetect(data.ix[x])   

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

            else:
                data.loc[data.index == x, 'box'] = -1
                data.loc[data.index == x, 'encoding'] = "Fail"

    # =========================================
    # 저장하기
    pickle.WritePickle(url, data)

    pickle.WritePickle(index_url, index)
    pickle.WritePickle(box_url, box)
    pickle.WritePickle(encoding_url, encoding)

    pickle.WritePickle(indexE_url, indexE)
    pickle.WritePickle(encodings_url, encodings)

    print(data)

