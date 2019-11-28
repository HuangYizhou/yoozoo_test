import cv2

from utilities.face_recog import recognizeFaces
from utilities.object_det import detectObjects
from utilities.drawing import draw_object_boxes, draw_face_boxes
from app import known_face_encodings, known_face_names, net, outputlayers, labels


def process(filename, face_confidence, object_confidence):
    input_movie = cv2.VideoCapture(f"uploads/{filename}")
    while True:
        # Grab a single frame of video
        ret, frame = input_movie.read()
        if not ret:
            break

        face_locations, face_names = recognizeFaces(frame, known_face_encodings, known_face_names, 0.25)
        boxes, confidences, classids, idxs = detectObjects(frame, net, outputlayers)

        frame = draw_face_boxes(frame, face_locations, face_names, 0.25)
        frame = draw_object_boxes(frame, boxes, confidences, classids, idxs, labels)

        yield frame
        # cv2.imshow("Video", frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
