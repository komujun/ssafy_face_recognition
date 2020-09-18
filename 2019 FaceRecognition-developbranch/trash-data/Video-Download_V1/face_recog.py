import face_api
import cv2
import os
import camera
import numpy as np

class FaceRecog():
    # 웹캠에서 아래 내용을 메모하고 비디오 파일을 사용합니다
    def __init__(self):
        self.camera = camera.VideoCamera()
        self.known_face_encodings = []
        self.known_face_names = []

        # 사진 로드, 인식 방법을 배운다
        dirname = 'knowns'
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_api.load_image_file(pathname)
                face_encoding = face_api.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def __del__(self):
        del self.camera

    def get_frame(self):
        # 비디오 한장씩 찍기
        frame = self.camera.get_frame()

        # 비디오 프레임을 1/4 크기로 조정
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # BGR -> RGB 변경
        rgb_small_frame = small_frame[:, :, ::-1]

        # 비디오 프레임만 처리하여 시간 절약
        if self.process_this_frame:
            # 얼굴과 얼굴 인코더를 찾는다
            self.face_locations = face_api.face_locations(rgb_small_frame)
            self.face_encodings = face_api.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # 얼굴이 알려진 얼굴과 일치하는지 확인한다
                distances = face_api.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # 0.6 대표적인 성는으로 테스트한다
                name = "Unknown"
                if min_value < 0.6:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        # 결과 표시
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # 얼굴 위치 다시 1/4로 축소
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # 얼굴에 상자를 그린다
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # 얼굴 라벨 그리기
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame

    def get_jpg_bytes(self):
        frame = self.get_frame()
        # 비디오 스트림
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


if __name__ == '__main__':
    face_recog = FaceRecog()
    print(face_recog.known_face_names)
    while True:
        frame = face_recog.get_frame()

        # 프레임 표시
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # q를 누르면 break
        if key == ord("q"):
            break

    # clear
    cv2.destroyAllWindows()
    print('finish')