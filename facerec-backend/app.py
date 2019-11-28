import threading
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__)
lock = threading.Lock()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

#cors = CORS(app, resources={r"/": {"origins": "http://localhost:5000"}})
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#load training faces
from utilities.file_preload import readFaces, readDarkNet
(known_face_encodings, known_face_names) = readFaces("TrainingFaces", [], [])
(net, outputlayers, labels) = readDarkNet("conf/yolov3-tiny.weights","conf/yolov3-tiny.cfg")



if __name__ == '__main__':
    from api import video_api, config_api, video_feed_api
    app.register_blueprint(video_api)
    app.register_blueprint(config_api)
    app.register_blueprint(video_feed_api)
    app.run()
