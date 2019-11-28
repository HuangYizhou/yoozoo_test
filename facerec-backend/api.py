from flask import request, Blueprint, Response
from models import Video, Config, videos_schema, config_schema
from app import db
import json
import cv2
from utilities.face_recog import recognizeFaces
from utilities.object_det import detectObjects
from utilities.drawing import draw_object_boxes, draw_face_boxes
from app import known_face_encodings, known_face_names, net, outputlayers, labels
from app import lock
from flask_cors import cross_origin

video_api = Blueprint('video', __name__)
@video_api.route('/video', methods=['GET','POST'])
@cross_origin(origin='localhost')
def video():
    if request.method == 'POST':
        static_file = request.files['video']
        static_file.save(f'./uploads/{static_file.filename}')
        video = Video(filename=static_file.filename)
        db.session.add(video)
        db.session.commit()
        db.session.flush()
        return f"Upload successful, video id {video.id}"
    elif request.method == 'GET':
        videos = Video.query.all()
        return json.dumps(videos_schema.dump(videos))


def gen(video_id):
    video_name = Video.query.filter_by(id=video_id).first().filename
    configuration = Config.query.first()
    input_movie = cv2.VideoCapture(f"uploads/{video_name}")

    while True:
        # Grab a single frame of video
        ret, frame = input_movie.read()
        if not ret:
            break

        face_locations, face_names = recognizeFaces(frame, known_face_encodings, known_face_names, configuration.face_confidence, 0.2)
        boxes, confidences, classids, idxs = detectObjects(frame, net, outputlayers, configuration.object_confidence)

        frame = draw_face_boxes(frame, face_locations, face_names, 0.2)
        frame = draw_object_boxes(frame, boxes, confidences, classids, idxs, labels)

        with lock:
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


video_feed_api = Blueprint('video_feed', __name__)
@video_feed_api.route('/video_feed/<int:video_id>')
def video_feed(video_id):
    return Response(gen(video_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




config_api = Blueprint('config', __name__)
@config_api.route('/config', methods=['GET','POST'])
@cross_origin(origin='localhost')
def config():
    if request.method == 'POST':
        config = db.session.query(Config).first()
        if config:
            config.object_confidence = request.json.get("object_confidence")
            config.face_confidence = request.json.get("face_confidence")
        else:
            config = Config(face_confidence=request.json.get("face_confidence"), object_confidence=request.json.get("object_confidence"))
        db.session.add(config)
        db.session.commit()
        db.session.flush()
        return f"Config update successfully"
    elif request.method == 'GET':
        config = db.session.query(Config).first()
        return json.dumps(config_schema.dump(config))
