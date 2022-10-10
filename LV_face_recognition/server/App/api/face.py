import numpy as np
from flask import request, Blueprint, jsonify, current_app
from KnnClass import KnnClass 
import const
from face_processing import extract_face, datagen, datagen_tf
from utils import _load_model
from sklearn.neighbors import KNeighborsClassifier
from datetime import datetime
from App.db import add_face, get_faces, delete_face
from matplotlib import pyplot

face_api_v1 = Blueprint(
    'face_api_v1', 'face_api_v1', url_prefix='/api/face')

facenet_keras_model = _load_model()
Knn = KnnClass()
# data = Knn.load_data_after_embedding(const.EMBDDINGS_FOLDER_EMB)
# X_train, X_test, y_train, y_test = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']


@face_api_v1.route("/predict", methods=["POST"])
def predict():  
  if request.method == 'POST':          
    # Lấy file ảnh người dùng upload lên
    image = request.files["image"]
    if image:
      # Extract feature
      image_array = extract_face(image, required_size=(160, 160))      
      if len(image_array) >= 1:
        faces, label = get_faces();
        knn_model = KNeighborsClassifier(n_neighbors=3, weights="distance", p=2) 
        knn_model.fit(faces, label) 
        # Embbding face
        image_embbeding = Knn.get_embedding(facenet_keras_model, image_array)    
        # Nomorlize
        image_embbeding = Knn.normalize_input_vectors([image_embbeding])  
        # Predict
        y_predict_test = knn_model.predict([image_embbeding[0]])
        return jsonify({"Label": y_predict_test[0]}), 200
      else:
        return jsonify({"msg": "File is so many people", }), 400
    else: 
      return jsonify({"error": "File not found", }), 400    

@face_api_v1.route("/train", methods=["POST"])
def train():
  if request.method == 'POST':
    _, labels = get_faces();
    user_name = request.form['user_name']
    uploaded_files = request.files.getlist("file[]")
    faces = []
    label = []
    
    if (len(list(filter (lambda x : x == user_name, labels))) > 0):
      return jsonify({"error": f"{user_name} is already exist" }), 400

    for file in uploaded_files:          
      image_array = extract_face(file, required_size=(160, 160))
      if len(image_array) >= 1:
        faces.append(image_array)
        label.append(user_name)
      else:
        return jsonify({"msg": f"File {file} is so many people", }), 400

    datagen.fit(faces)
    X_au = []
    y_au = []
    for i in np.arange(len(faces)):
      no_img = 0
      for x in datagen.flow(np.expand_dims(faces[i], axis = 0), batch_size = 1):
        X_au.append(x[0])
        y_au.append(label[i])
        no_img += 1
        if no_img == 16:
          break

    newTrainX = list()
    for face_pixels in X_au:
      embedding = Knn.get_embedding(facenet_keras_model, face_pixels)
      newTrainX.append(embedding)
    newTrainX = np.asarray(newTrainX)
    print(newTrainX.shape)

    newTrainX = Knn.normalize_input_vectors(newTrainX)

    for i in range(len(newTrainX)):    
      add_face(newTrainX[i].tolist() , user_name) 

    return jsonify({"msg": f"Training {user_name} success" })

@face_api_v1.route("/init_data", methods=["GET"])
def init_data():  
  # normalize_input_vectors
  X_new_train = Knn.normalize_input_vectors(current_app.X_train)
  X_new_test = Knn.normalize_input_vectors(current_app.X_test)
  
  for i in range(len(X_new_train)):
        # face_embedding = FaceEmbeddings(
    #   face_embedding=X_data[i],
    #   label=y_data[i]
    # )
    # face_embedding.save()
    add_face(X_new_train[i].tolist() , y_train[i])

  for i in range(len(X_new_test)):
        # face_embedding = FaceEmbeddings(
    #   face_embedding=X_data[i],
    #   label=y_data[i]
    # )
    # face_embedding.save()
    add_face(X_new_train[i].tolist() , y_test[i])  

  return jsonify({"msg":f"Add vector to database" })

@face_api_v1.route("/get_faces", methods=["GET"])
def get_face():
  faces, labels = get_faces()
  
  return jsonify({"msg":f"Get {len(faces)} success" })

@face_api_v1.route("/test", methods=["GET"])
def delete_face():
  return jsonify({"msg":f"hello world" })

@face_api_v1.route("/delete_label", methods=["POST"])
def delete_face_label():
  if request.method == 'POST':    
    userName = request.form['username']
    if userName:    
      delete_face(userName)     
      return jsonify({"msg":f"delete {userName} success" }), 200 
    else:
      return jsonify({"msg":f"{userName} not found" }), 400   


