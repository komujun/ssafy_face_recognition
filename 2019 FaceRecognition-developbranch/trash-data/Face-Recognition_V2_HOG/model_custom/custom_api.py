# -*- coding: utf-8 -*-
import PIL.Image
import dlib
import numpy as np
import face_recognition_models as models

# ====================================================================================================================
# models에 있는 모델 변수 적용
face_detector = dlib.get_frontal_face_detector()

point_68_predictor = models.pose_predictor_model_location()
point_68_pose = dlib.shape_predictor(point_68_predictor)

point_5_predictor = models.pose_predictor_five_point_model_location()
point_5_pose = dlib.shape_predictor(point_5_predictor)

face_detection_model = models.cnn_face_detector_model_location()
face_detector_tool = dlib.cnn_face_detection_model_v1(face_detection_model)

face_recognition_model = models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)


# ====================================================================================================================
# dlib 'rect' 객체를 top, right, bottom, left 순서로 변환
# param rect : dlib 'rect' 오브젝트
# return : tuple (top, right, bottom, left)
def _rect_to_css(rect):
    return rect.top(), rect.right(), rect.bottom(), rect.left()


# tuple (top, right, bottom, left) -> dlib 'rect' 객체 변환
# param css : tuple (t, r, b, l)
# return : dlib 'rect' 오브젝트
def _css_to_rect(css):
    return dlib.rectangle(css[3], css[0], css[1], css[2])


# ====================================================================================================================
# (top, right, bottom, left) 순서로 dlib 'rect' 오브젝트가 지정된 범위에 있는지 확인
# param css : tuple (t, r, b, l)
# param image_shape : numpy image array
# return : tuple (t, r, b, l)
def _trim_css_to_bounds(css, image_shape):
    return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)


# ====================================================================================================================
# 얼굴 인코딩의 목록이 주어지면, 유클리드상 거리를 구한다.
# 거리는 얼굴들 간에 얼마나 비슷한지 알려준다.
# param face_encodings : 비교할 얼굴 인코딩 목록
# param face_to_compare : 비교할 얼굴 인코딩
# return : 각 면의 길이를 반환 (numpy array)
def face_distance(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))

    return np.linalg.norm(face_encodings - face_to_compare, axis=1)


# ====================================================================================================================
# .jpg, .png 파일을 numpy array으로 업로드 한다.
# param file : 로드할 이미지 파일 이름 또는 객체
# param mode : 이미지를 변환할 형식 (RGB혹은 L 가능)
# return : 이미지파일을 numpy array로 변환
def load_image_file(file, mode='RGB'):
    im = PIL.Image.open(file)
    if mode:
        im = im.convert(mode)
    return np.array(im)


# ====================================================================================================================
# image에서 경계 상자 배열을 반환한다.
# param img : 이미지 (numpy array)
# param number_of_time_to_upsample : 면을 찾는 이미지를 sampling 하는 횟수, 많아질 수록 사진이 작아진다
# model : 사용할 얼굴 검출 모델, cnn이 더 정확하나, 여기서는 HOG 알고리즘을 사용한다.
# return : 검출한 경계 상자 배열 -> dlib 상자 리스트
def _raw_face_locations(img, number_of_times_to_upsample=1, model="hog"):
    if model == "cnn":
        return face_detector_tool(img, number_of_times_to_upsample)
    else:
        return face_detector(img, number_of_times_to_upsample)


# image에서 경계 상자 배열을 반환한다.
# param img : 이미지 (numpy array)
# param number_of_time_to_upsample : 면을 찾는 이미지를 sampling 하는 횟수, 많아질 수록 사진이 작아진다
# model : 사용할 얼굴 검출 모델, cnn이 더 정확하나, 여기서는 HOG 알고리즘을 사용한다.
# return : 검출한 경계 상자 배열 -> dlib 상자 리스트
def face_locations(img, number_of_times_to_upsample=1, model="hog"):
    if model == "cnn":
        return [_trim_css_to_bounds(_rect_to_css(face.rect), img.shape) for face in _raw_face_locations(img, number_of_times_to_upsample, "cnn")]
    else:
        return [_trim_css_to_bounds(_rect_to_css(face), img.shape) for face in _raw_face_locations(img, number_of_times_to_upsample, model)]


# ====================================================================================================================
# cnn 얼굴 검출을 사용해서 영상의 사람 2d 배열이 반환된다
# param img : 이미지 (numpy array)
# param number_of_time_to_upsample : 면을 찾는 이미지를 sampling 하는 횟수, 많아질 수록 사진이 작아진다
# return : 검출한 경계 상자 배열 -> dlib 상자 리스트
def _raw_face_locations_batched(images, number_of_times_to_upsample=1, batch_size=128):
    return face_detector_tool(images, number_of_times_to_upsample, batch_size=batch_size)


# cnn 얼굴 검출을 사용해서 영상의 사람 2d 배열이 반환된다
# GPU를 사용하지 않는 경우에는 이 기능이 필요하지 않습니다.
# param img : 이미지 (numpy array)
# param number_of_time_to_upsample : 면을 찾는 이미지를 sampling 하는 횟수, 많아질 수록 사진이 작아진다
# param batch_size : 각 GPU 처리 배치에 포함할 이미지 수
# return : css(top, right, bottom, left) 얼굴 위치의 2배 목록
def batch_face_locations(images, number_of_times_to_upsample=1, batch_size=128):
    def convert_cnn_detections_to_css(detections):
        return [_trim_css_to_bounds(_rect_to_css(face.rect), images[0].shape) for face in detections]

    raw_detections_batched = _raw_face_locations_batched(images, number_of_times_to_upsample, batch_size)

    return list(map(convert_cnn_detections_to_css, raw_detections_batched))


# ====================================================================================================================
# image의 각 면에 대한 얼굴 특징 위치 (눈, 코 등) 의 위치를 반환한다
# param face_image: 검색할 이미지
# param face_locations: 선택적으로 확인할 면 위치 목록을 제공한다
# param model : 사용할 모델, 5 포인트만 반환하지만 large, small 옵션이 있습니다.
# return : 얼굴 위치의 목록 (눈, 코 등)
def _raw_face_landmarks(face_image, face_locations=None, model="large"):
    if face_locations is None:
        face_locations = _raw_face_locations(face_image)
    else:
        face_locations = [_css_to_rect(face_location) for face_location in face_locations]

    pose_predictor = point_68_pose

    if model == "small":
        pose_predictor = point_5_pose

    return [pose_predictor(face_image, face_location) for face_location in face_locations]


# image의 각 면에 대한 얼굴 특징 위치 (눈, 코 등) 의 위치를 반환한다
# param face_image: 검색할 이미지
# param face_locations: 선택적으로 확인할 면 위치 목록을 제공한다
# param model : 사용할 모델, 5 포인트만 반환하지만 large, small 옵션이 있습니다.
# return : 얼굴 위치의 목록 (눈, 코 등)
def face_landmarks(face_image, face_locations=None, model="large"):
    landmarks = _raw_face_landmarks(face_image, face_locations, model)
    landmarks_as_tuples = [[(p.x, p.y) for p in landmark.parts()] for landmark in landmarks]

    # For a definition of each point index, see https://cdn-images-1.medium.com/max/1600/1*AbEg31EgkbXSQehuNJBlWg.png
    if model == 'large':
        return [{
            "chin": points[0:17],
            "left_eyebrow": points[17:22],
            "right_eyebrow": points[22:27],
            "nose_bridge": points[27:31],
            "nose_tip": points[31:36],
            "left_eye": points[36:42],
            "right_eye": points[42:48],
            "top_lip": points[48:55] + [points[64]] + [points[63]] + [points[62]] + [points[61]] + [points[60]],
            "bottom_lip": points[54:60] + [points[48]] + [points[60]] + [points[67]] + [points[66]] + [points[65]] + [points[64]]
        } for points in landmarks_as_tuples]
    elif model == 'small':
        return [{
            "nose_tip": [points[4]],
            "left_eye": points[2:4],
            "right_eye": points[0:2],
        } for points in landmarks_as_tuples]
    else:
        raise ValueError("Invalid landmarks model type. Supported models are ['small', 'large'].")


# ====================================================================================================================
# 이미지를 지정한 경우, 이미지의 각 면에 대해 128차원 인코딩을 반환한다
# param face_image: 하나 이상의 면을 포함하는 이미지
# param alert_face_locations: 각 면의 경계사항 (선택 사항)
# param num_jeters : 얼굴을 다시 샘플링하는 횟수, 더 높은것이 정확하지만 느리다. (100배는 100배 느림)
# return : 128차원 페이스 인코딩 리스트 (면마다 하나씩)
def face_encodings(face_image, known_face_locations=None, num_jitters=1):
    raw_landmarks = _raw_face_landmarks(face_image, known_face_locations, model="small")
    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]


# ====================================================================================================================
# 얼굴 인코딩 목록과 후보 인코딩을 비교하여 일치하는지 확인
# param alert_face_encodings: 얼굴 인코딩 목록
# param face_encoding_to_check : 단일 면 인코딩을 사용하여 리스트와 비교
# 모수 공차 : 면 사이의 거리, 0.6은 전형적인 수치
# return True/False 값 리스트
def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    return list(face_distance(known_face_encodings, face_encoding_to_check) <= tolerance)