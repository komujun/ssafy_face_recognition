import json
import requests

url = "https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/albums/1/pictures/1/children/3"

json_test = {}
json_data = {
  "child_id": 1,
  "rect_x": 24,
  "rect_y": 34,
  "rect_width": 125,
  "rect_height": 146
}

# json_string = json.dumps(json_data).encode("utf-8")
# response = requests.post(url, data=json_string)

json_data2 = {
  "child_id": 2,
  "rect_x": 24,
  "rect_y": 34,
  "rect_width": 125,
  "rect_height": 148
}

# json_string = json.dumps(json_data2).encode("utf-8")
# response = requests.post(url, data=json_string)

print(json_test)
json_test.update(json_data)
print(json_test)
json_test.update(json_data2)
print(json_test)

json_string = json.dumps(json_data).encode("utf-8")

# response = requests.post(url, data=json_string)
response = requests.delete(url)

# print(response.json())