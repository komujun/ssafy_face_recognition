import requests
import json
import picture_class
import picture_download
import picture_detect
import picture_search

# url get
try:
    url = 'https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/pictures/processing'
    response = requests.get(url)
except:
    print("URL 주소가 잘못되었습니다")

# data get
try:
    data = picture_class.picture_data()
    data.append_data(response)
except:
    print("사이트를 읽는데 실패하였습니다")
    
# picture download
try:
    for i in range(0, data.getLen()):
        album_id = str(data.getAlbumId(i)).strip()
        picture_id = str(data.getPictureId(i)).strip()
        status = data.getStatus(i)
        picture_url = str(data.getPictureUrl(i)).strip()

        # print(album_id, picture_id, status, picture_url)
        download = picture_download.getDownload(album_id, picture_id, status, picture_url)
except:
    print("사진을 저장하는데 실패하였습니다.")

# picture detecting
try:
    for i in range(0, data.getLen()):
        print(i)
        album_id = str(data.getAlbumId(i)).strip()
        picture_id = str(data.getPictureId(i)).strip()
        status = data.getStatus(i)
        picture_url = str(data.getPictureUrl(i)).strip()

        print(album_id, picture_id, status, picture_url)
        img_before, img_after = picture_search.faceSearch(album_id, picture_id, status, picture_url)
        if(img_before != -1 and img_after != -1):
             checking = picture_detect.faceDetect(album_id, picture_id, status, picture_url, img_before, img_after)

        checking = 1
        if(checking == 1):
            put_url = "https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/albums/" + str(album_id) + "/pictures/" + str(picture_id)
        
        json_data = {
             "status" : 'processing'
        }
            
        json_string = json.dumps(json_data).encode("utf-8")
        response = requests.put(put_url, data=json_string)

        json_data = {
           "status" : "checking"
        } 
        json_string = json.dumps(json_data).encode("utf-8")
        response = requests.put(put_url, data=json_string) 

except:
    print("사진을 처리하는데 실패하였습니다.")