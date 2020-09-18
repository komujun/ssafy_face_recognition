#!/usr/bin/env python3
from __future__ import print_function
import face_recognition
import cv2
from sklearn.cluster import DBSCAN
import numpy as np
import os
import pickle
import signal
import sys

class Face():
    def __init__(self, picture_id, name, box, encoding):
        self.frame_id = frame_id
        self.name = name
        self.box = box
        self.encoding = encoding


class FaceClustering():
    def __init__(self):
        self.faces = []
        self.run_encoding = False
        self.picutre_dir = "pictures"

    def capture_filename(self, frame_id):
        return "frame_%08d.jpg" % frame_id

    def signal_handler(self, sig, frame):
        print(" stop encoding.")
        self.run_encoding = False

    def drawBoxes(self, frame, faces_in_frame):
        # Draw a box around the face
        for face in faces_in_frame:
            (top, right, bottom, left) = face.box
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)