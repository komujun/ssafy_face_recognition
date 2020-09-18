import urllib.request

def getDownload(file_name, img):

    try:
        urllib.request.urlretrieve(img, "./img/" + file_name)
        print(file_name + " " + img + " 다운로드 완료!")
        return true
    except:
        return false
    