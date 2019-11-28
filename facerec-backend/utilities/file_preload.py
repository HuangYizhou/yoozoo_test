#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 11:40:23 2019

@author: Yizhou
"""

from pathlib import Path
import face_recognition
import cv2

def readFaces(root, known_face_names, known_face_encodings):
	known_face_names = []
	known_face_encodings = []
	for file in Path(root).glob('*/*.jpg'):
		try:
			face_image = face_recognition.load_image_file(file)
			face_encoding = face_recognition.face_encodings(face_image)[0]

			known_face_encodings.append(face_encoding)
			known_face_names.append(file.parent.name)

		except Exception as e:
			pass

	return (known_face_encodings, known_face_names)

def readDarkNet(weight_path, cfg_path):
	net = cv2.dnn.readNet(weight_path, cfg_path)
	layer_names = net.getLayerNames()
	outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

	labels = []
	with open("conf/coco.names","r") as f:
		labels = [line.strip() for line in f.readlines()]

	return (net, outputlayers, labels)