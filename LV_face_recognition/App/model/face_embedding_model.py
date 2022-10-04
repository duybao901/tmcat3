from mongoengine import *

class FaceEmbeddings(Document):
    face_embedding = ListField(required=True, max_length=128)
    label = StringField(required=True, unique=True, max_length=50)

    def to_json(self):
        return {
        "face_emdding": self.face_embedding,
        "label": self.label
        }