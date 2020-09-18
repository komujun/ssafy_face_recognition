import json
import requests

def clear():
    base_url = "https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/albums/"

    i = 0
    while True:
        i += 1
        j = 0

        while True:
            j += 1
            url = base_url + str(i) + "/pictures/" + str(j)
            response = requests.get(url)
            # print(response.json())

            count = len(response.json())
            print(response.json())
            if(count == 1):
                break
            '''
            else:
                json_data = {
                    "status" : "processing"
                }
                json_string = json.dumps(json_data).encode("utf-8")
                response = requests.put(url, data=json_string)
            '''
            
        if(count == 1 and j == 1):
            break

clear()