class Picture_ID:
    # 사진 변수 초기화
    def __init__(self):
        self.album_id = []
        self.picture_id = []
        self.file_name = []
        self.status = []
        self.picture_url = []
    
    # 앨범 데이터 추가
    def append_id(self, response):
        for i in response.json():
            self.album_id.append(i['album_id'])
            self.picture_id.append(i['picture_id'])
            self.file_name.append(i['file_name'])
            self.status.append(i['status'])
            self.picture_url.append(i['picture_url'])

    # URL 추가
    def print_id(self):
        for i in range(len(self.picture_url)):
            print(self.picture_url[i])

    # 초기화
    def destroy_id(self):
        self.album_id = []
        self.picture_id = []
        self.file_name = []
        self.status = []
        self.picture_url = []

    # 앨범 아이디 호출
    def getAlbumId(self, x):
        return self.album_id[x]

    # 사진 아이디 호출
    def getPictureId(self, x):
        return self.picture_id[x]

    # 사진 이름 호출
    def getFileName(self, x):
        return self.file_name[x]

    # status 호출
    def getStatus(self, x):
        return self.status[x]

    # 사진 URL 호출
    def getPictureUrl(self, x):
        return self.picture_url[x]