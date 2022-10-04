
import numpy as np
from flask import request, Blueprint, jsonify
from KnnClass import KnnClass 
import const
from face_processing import extract_face, datagen, datagen_tf
from utils import _load_model
from sklearn.neighbors import KNeighborsClassifier
from datetime import datetime
from App.db import add_face
from App.model.face_embedding_model import FaceEmbeddings

face_api_v1 = Blueprint(
    'face_api_v1', 'face_api_v1', url_prefix='/api/face')

facenet_keras_model = _load_model()
Knn = KnnClass()
data = Knn.load_data_after_embedding(const.EMBDDINGS_FOLDER_EMB)

X_train, X_test, y_train, y_test = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']

# normalize_input_vectors
# X_train = Knn.normalize_input_vectors(X_train)
# X_test = Knn.normalize_input_vectors(X_test)

# print(X_train)


knn_model = KNeighborsClassifier(n_neighbors=3, weights="distance", p=2) 
knn_model.fit(X_train, y_train)    

@face_api_v1.route("/predict", methods=["POST"])
def predict():  
  if request.method == 'POST':  
    # Lấy file ảnh người dùng upload lên
    image = request.files["image"]
    # Extract feature
    image_array = extract_face(image, required_size=(160, 160))
    # Embbding face
    image_embbeding = Knn.get_embedding(facenet_keras_model, image_array)    
    # Predict
    y_predict_test = knn_model.predict([image_embbeding])
    return jsonify({"Label": y_predict_test[0]}), 200

@face_api_v1.route("/train", methods=["POST"])
def train():
  if request.method == 'POST':
    user_name = request.form['user_name']
    uploaded_files = request.files.getlist("file[]")
    faces = []
    label = []
    for file in uploaded_files:          
      image_array = extract_face(file, required_size=(160, 160))
      if(image_array == []):
        return jsonify({"msg": "Fails to extract file " + user_name})
      faces.append(image_array)
      label.append(user_name)

    X_new_train, X_new_test, y_new_train, y_new_test = Knn.split_data(faces, label)

    datagen.fit(X_new_train)
    X_au = []
    y_au = []
    for i in np.arange(len(X_new_train)):
      no_img = 0
      for x in datagen.flow(np.expand_dims(X_new_train[i], axis = 0), batch_size = 1):
        X_au.append(x[0])
        y_au.append(y_new_train[i])
        no_img += 1
        if no_img == 16:
          break

    datagen_tf.fit(X_new_test)
    X_new_test_tf = []
    for i in np.arange(len(X_new_test)):
      no_img = 0
      for x in datagen_tf.flow(np.expand_dims(X_new_test[i], axis = 0), batch_size = 1):
        X_new_test_tf.append(x[0])
        no_img += 1
        if no_img == 1:
          break
    newTrainX = list()
    for face_pixels in X_au:
      embedding = Knn.get_embedding(facenet_keras_model, face_pixels)
      newTrainX.append(embedding)
    newTrainX = np.asarray(newTrainX)
    print(newTrainX.shape)

    newTestX = list()
    for face_pixels in X_new_test_tf:
      embedding = Knn.get_embedding(facenet_keras_model, face_pixels)
      newTestX.append(embedding)
    newTestX = np.asarray(newTestX)
    print(newTestX.shape)

    return jsonify({"msg": f"Training {user_name} success" })

@face_api_v1.route("/init_data", methods=["GET"])
def init_data():  
  X_data = np.concatenate((X_train, X_test), axis=0)
  y_data = np.concatenate((y_train, y_test), axis=0) 
  
  for i in range(len(X_data)):
    face_embedding = FaceEmbeddings(
      face_embedding=X_data[i],
      label=y_data[i]
    )
    # face_embedding.save()
    add_face(X_data[i].tolist() , y_data[i])

  return jsonify({"msg":f"Add {len(X_data)} vector to database" })

