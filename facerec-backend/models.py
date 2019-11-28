
from app import db, ma


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Video %r>' % self.filename


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    face_confidence = db.Column(db.Float, nullable=True)
    object_confidence = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"Face confidence: {self.face_confidence}. Object confidence: {self.object_confidence}"


class ConfigSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "face_confidence", "object_confidence")


class VideoSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "filename")


video_schema = VideoSchema()
videos_schema = VideoSchema(many=True)
config_schema = ConfigSchema()
configs_schema = ConfigSchema(many=True)