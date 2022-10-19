import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo

from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

# class FaceEmbeddings(db.Document):
#     image_array = db.Arra

def add_face(face_embdding, label):
    """    
    - "face_embdding"
    - "label"
    """    
    face = { 'face_embdding' : face_embdding, "label": label}
    return db.image_normalizes.insert_one(face)

def get_faces():

    faces_embeddings = []
    labels = []
    for doc in db.image_normalizes.find({}):
        # print(doc.face_embdding)
        faces_embeddings.append(doc["face_embdding"])
        labels.append(doc["label"])
    return faces_embeddings, labels

# def delete_image():
#     query = {"label":"pil"}
#     return db.image_normalizes.delete_many(query)


def delete_face(face):
    query = {"label":face}
    return db.image_normalizes.delete_many(query)

def find_by_username(username):
     query = {"label": username}
     return db.image_normalizes.find_one(query)

def get_faces_by_username(userName):
    query = {"label": userName}
    return db.image_normalizes.find(query)