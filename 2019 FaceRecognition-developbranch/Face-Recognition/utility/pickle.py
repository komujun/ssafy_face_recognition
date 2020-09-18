import pickle
import gzip

def ReadPickle(url):
    file = gzip.open(url, "rb")
    temp = pickle.load(file)
    file.close()
    
    return temp

def WritePickle(url, data):
    file = gzip.open(url, "wb")
    pickle.dump(data, file)
    file.close()