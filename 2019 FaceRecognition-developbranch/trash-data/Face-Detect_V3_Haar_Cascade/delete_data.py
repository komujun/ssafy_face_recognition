import json
import requests

for i in range(1, 10):
  for j in range(1, 100):
    url = "https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/albums/" + str(i) + "/pictures/" + str(j)

    json_data = {
      "status" : "processing"
    }

    json_string = json.dumps(json_data).encode("utf-8")
    response = requests.put(url, data=json_string)

    print(response.json())