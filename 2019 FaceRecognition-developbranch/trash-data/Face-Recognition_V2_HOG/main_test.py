import json
import requests
import pickle
from picture_utility import picture_class as pc
from picture_utility import picture_download as pdl
from picture_utility import picture_detect as pdt
from picture_utility import picture_pickle as pp
from clustering_utility import face_clustering as fc

# https://docs.google.com/document/d/1lwofKqyqlq--8LuiqjpFgP4R-7mPNt0JT5QwAcu_MRA/edit
# FaceRecognition <-> Server

# https://kidsharu.github.io/KidsHaru-APIDoc/
# 자세한 API 문서

# picture pickle
data2 = pc.picture_data()
pp.WritePickle(data2)
