import json
import requests
import pickle
import gzip

def ReadPickle(data2):
    path = "./picture_utility/picture_pickle/picture_class.pickle"
    file = gzip.open(path, "rb")
    temp = pickle.load(file)
    # print(temp)
    file.close()
    
    for i in range(temp.getLen()):
        data2.setAlbumId(temp.getAlbumId(i))
        data2.setPictureId(temp.getPictureId(i))
        data2.setPictureIdData(temp.getPictureIdData(i))
        data2.setStatus(temp.getStatus(i))
        data2.setPictureUrl(temp.getPictureUrl(i))
        data2.setPictureCut(temp.getPictureCut(i))
        data2.setBox(temp.getBox(i))
        data2.setEncoding(temp.getEncoding(i))
        # print('데이터 불러오기 완료!')


def WritePickle(data2):
    path = "./picture_utility/picture_pickle/picture_class.pickle"
    file = gzip.open(path, "wb")
    pickle.dump(data2, file)
    # print(file)
    file.close()


def WriteAppendFile(data, data2, i):
    data2.setAlbumId(data.getAlbumId(i))
    data2.setPictureId(data.getPictureId(i))
    data2.setPictureIdData(data.getPictureIdData(i))
    data2.setStatus(data.getStatus(i))
    data2.setPictureUrl(data.getPictureUrl(i))
    data2.setPictureCut(data.getPictureCut(i))
    data2.setBox(data.getBox(i))
    data2.setEncoding(data.getEncoding(i))
    # print('데이터 저장 완료!')