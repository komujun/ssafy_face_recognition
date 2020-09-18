class picture_data:
    # picture_class init
    def __init__(self):
        self.album_id = []      # album_id
        self.picture_id = []    # picture_id
        self.status = []        # status (processing)
        self.picture_url = []   # picture_url (http:// ... .jpg)
        print("생성되었습니다")

    # picture_class destory
    def __del__(self):
        print("삭제되었습니다")

    # picture_data_append
    def append_data(self, response):
        for i in response.json():
            self.album_id.append(i['album_id'])
            self.picture_id.append(i['picture_id'])
            self.status.append(i['status'])
            self.picture_url.append(i['picture_url'])

    # file set
    def setAlbumId(self, x, data):
        self.album_id[x] = data

    def setPictureId(self, x, data):
        self.picture_id[x] = data

    def setStatus(self, x, data):
        self.status[x] = data

    def setPictureUrl(self, x, data):
        self.picture_url[x] = data

    # file get
    def getAlbumId(self, x):
        return self.album_id[x]

    def getPictureId(self, x):
        return self.picture_id[x]

    def getStatus(self, x):
        return self.status[x]

    def getPictureUrl(self, x):
        return self.picture_url[x]

    def getLen(self):
        return len(self.album_id)

    # print data
    def print_id(self, start, end):
        for i in range(start, end):
            print(self.album_id[i])
            print(self.picture_id[i])
            print(self.status[i])
            print(self.picture_url[i])