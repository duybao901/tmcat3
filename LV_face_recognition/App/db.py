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
    Inserts a comment into the comments collection, with the following fields:
    - "name"
    - "email"
    - "movie_id"
    - "text"
    - "date"
    Name and email must be retrieved from the "user" object.
    """    
    face = { 'face_embdding' : face_embdding, "label": label}
    return db.image_embeddings.insert_one(face)