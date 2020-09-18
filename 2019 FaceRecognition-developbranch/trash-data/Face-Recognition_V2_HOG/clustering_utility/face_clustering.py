from sklearn.cluster import DBSCAN
import pickle
import numpy as np
import os
import signal
import sys
import cv2
import model_custom
from picture_utility import picture_class as pc
import shutil
import gzip

def clustering(data2):
    cnt = 0
    name = []
    img = []
    encodings = []

    path = "./clustering_utility/clustering_class.pickle"
    file = gzip.open(path, "wb")
    pickle.dump(encodings, file)
    file.close()

    cnt = 0
    for i in range(data2.getLen()):
        if data2.getEncoding(i) != []:
            for j in range(len(data2.getEncoding(i))):
                # print(data2.getPictureCut(i)[j])
                img.append(data2.getPictureCut(i)[j])
                encodings.append(data2.getEncoding(i)[j])

    path = "./clustering_utility/clustering_class.pickle"
    file = gzip.open(path, "wb")
    pickle.dump(encodings, file)
    file.close()

    # for i in range(len(img)):
        #print(img[i].split('/')[4])
    
    # cluster the embeddings
    clt = DBSCAN(eps=0.2, min_samples=3, metric="euclidean")
    X = clt.fit(encodings)
    print(X)

    # label 결정
    label_ids = np.unique(clt.labels_)
    num_unique_faces = len(np.where(label_ids > -1)[0])
    print("clustered %d unique faces." % num_unique_faces)
    # print(len(label_ids))

    if os.path.isdir("./clustering_utility/ID"):
        shutil.rmtree("./clustering_utility/ID")

    path = "./clustering_utility/ID/"
    for label_id in label_ids:
        dir_name = "ID%d" % label_id
        print(dir_name)

        if not os.path.isdir(path):
            os.mkdir(path)

        if not os.path.isdir(path + dir_name):
            os.mkdir(path + dir_name)

        # find all indexes of label_id
        indexes = np.where(clt.labels_ == label_id)[0]
        # print(indexes)

        # save face images
        for i in indexes:
            image = cv2.imread(img[i])
        
            url_path = path + dir_name + "/" + img[i].split('/')[3] + "_" + img[i].split('/')[4]
            # print(url_path, img[i])
            # print(i)

            cv2.imwrite(url_path, image)
    print('clustering done')
