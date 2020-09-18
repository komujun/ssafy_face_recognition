import json
import requests
import pickle

for i in range(500):
    post_url = "https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/faces/" + str(i)
    response = requests.delete(post_url)
