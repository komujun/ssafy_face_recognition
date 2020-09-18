import os
import sys
from pandas import Series, DataFrame
from utility import pickle

def picture_saving(url, data):
    data_temp = DataFrame({})
    temp = DataFrame({})

    if os.path.isfile(url):
        data_temp = pickle.ReadPickle(url)
        print('pickle 로드 완료!')

        if len(data_temp) > 0:
            for x in range(len(data)):
                url_temp = data.ix[x]['picture_url']
                name_temp = data.ix[x]['picture_name']

                arr2 = []
                try:
                    arr1 = data_temp.loc[data_temp['picture_url'] == url_temp]
                    if len(arr1) > 0:
                        arr2 = arr1.loc[arr1['picture_name'] == name_temp]
                except:
                    pass
                
                if len(arr2) < 1:
                    data_temp = data_temp.append(data.ix[x], ignore_index = True)
            
            pickle.WritePickle(url, data_temp)
            print('pickle 저장 완료!')

        else:
            pickle.WritePickle(url, data)
            print('pickle 저장 완료!')

    else:
        pickle.WritePickle(url, temp)
        print('pickle 저장 완료!')

    return data_temp, data


def util_saving(name, url):
    temp = []

    if os.path.isfile(url):
        temp = pickle.ReadPickle(url)
        # print(name, 'pickle 로드 완료!')

    else:
        pickle.WritePickle(url, temp)
        # print(name, 'pickle 저장 완료!')

    return temp
