import requests
import Picture_detect
import Picture_class
import Picture_download

url = 'https://fc3i3hiwel.execute-api.ap-northeast-2.amazonaws.com/develop/pictures/processing'
response = requests.get(url)

try:
    data = Picture_class.Picture_ID()
    data.append_id(response)
except:
    print("사이트를 읽는데 실패하였습니다.")

Picture_download.getDownload(str(data.getFileName(0)).strip(), str(data.getPictureUrl(0)).strip())

try:
    faceDetect(str(data.getPictureUrl(0)).strip())
except:
    print("이미지를 처리하는데 실패했습니다.")

# data.print_id(response)