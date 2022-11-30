import numpy as np
from flask import request, Blueprint, jsonify, current_app, make_response
from KnnClass import KnnClass 
from face_processing import extract_face_mtcnn, datagen, datagen_tf
from utils import _load_model
from sklearn.neighbors import KNeighborsClassifier
from datetime import datetime
from App.db import add_face, get_faces, delete_face, find_by_username, get_faces_by_username

face_api_v1 = Blueprint(
    'face_api_v1', 'face_api_v1', url_prefix='/api/face')


facenet_keras_model = _load_model()

Knn = KnnClass()
# data = Knn.load_data_after_embedding(const.EMBDDINGS_FOLDER_EMB)
# X_train, X_test, y_train, y_test = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']

@face_api_v1.route("/login", methods=["POST"])
def predict():  
  if request.method == 'POST':    
    response = jsonify()      
    # Lấy file ảnh người dùng upload lên
    image = request.files["file"]
    redirect_url = request.form['redirect_url']
    
    if image:
      # Extract feature
      image_array = extract_face_mtcnn(image, required_size=(160, 160))   
      datagen_tf.fit([image_array])
      # Data Augumentation
      X_datagen =  datagen_tf.flow(np.expand_dims(image_array, axis = 0), batch_size = 1)
      image_array = X_datagen[0][0]
      if len(image_array) >= 1:
        faces, label = get_faces();
        knn_model = KNeighborsClassifier(n_neighbors=5, weights="distance", p=2) 
        knn_model.fit(faces, label) 
        # Embbding face
        image_embbeding = Knn.get_embedding(facenet_keras_model, image_array)    
        # Nomorlize
        image_embbeding = Knn.normalize_input_vectors([image_embbeding])  
        # Predict
        y_predict_test = knn_model.predict([image_embbeding[0]])

        response = make_response(
              jsonify({"email": y_predict_test[0], "redirect_url": redirect_url + f"?email={y_predict_test[0]}"}), 200)
        # response = make_response(
        #       jsonify({"email": "a", "redirect_url": redirect_url + f"?email=a"}), 200)
        # print("user_name", y_predict_test[0])
        # print("redirect_url", redirect_url)

        # # response._status_code = 301
        # response.headers['location'] = redirect_url + f"?email={y_predict_test[0]}"
        # response.headers.add('Access-Control-Allow-Origin', '*')
        # response.autocorrect_location_header = False
        return response

      else:
        return jsonify({"msg": "File is so many people", "redirect_url": redirect_url + f"?error=file-is-so-many-people" }), 400
    else: 
      return jsonify({"msg": "File not found", "redirect_url": redirect_url + f"?error=file-not-found" }), 400    

@face_api_v1.route("/register", methods=["POST"])
def train():
  if request.method == 'POST':
    user_name = request.form['user_name']
    redirect_url = request.form['redirect_url']
    uploaded_files = request.files.getlist("file")
    faces = []
    label = []

    response = jsonify()

    _, labels = get_faces();
    
    if (len(list(filter (lambda x : x == user_name, labels))) > 0):
      response = make_response(
          jsonify({"msg": f"{user_name} đã tồn tại",  "redirect_url": redirect_url + f"?error=user-is-exits"}), 
          400)

      # response.headers['location'] = redirect_url + f"?error={user_name}-is-exits"
      return response
    
    for file in uploaded_files:       
      image_array = extract_face(file, required_size=(160, 160))
      if len(image_array) >= 1:
        faces.append(image_array)
        label.append(user_name)
      else:
        response = make_response(
          jsonify({"msg": f"File {file.filename} có quá nhiều người", "redirect_url": redirect_url + f"?error=file-is-so-many-people"}), 
          400)

        # response.headers['location'] = redirect_url + f"?error=file-have-many-people"
        return response
    
    numberGenerator = 8;
    
    datagen.fit(faces)
    X_au = []
    y_au = []
    for i in np.arange(len(faces)):
      no_img = 0
      for x in datagen.flow(np.expand_dims(faces[i], axis = 0), batch_size = 1):
        X_au.append(x[0])
        y_au.append(label[i])
        no_img += 1
        if no_img == numberGenerator:
          break

    newTrainX = list()
    for face_pixels in X_au:
      embedding = Knn.get_embedding(facenet_keras_model, face_pixels)
      newTrainX.append(embedding)
    newTrainX = np.asarray(newTrainX)

    newTrainX = Knn.normalize_input_vectors(newTrainX)

    # Add to database
    for i in range(len(newTrainX)):    
      add_face(newTrainX[i].tolist() , user_name) 

    response = make_response(
              jsonify({"email": user_name, "redirect_url": redirect_url + f"?email={user_name}"}), 200)

    # print("user_name", user_name)
    # print("redirect_url", redirect_url)

    # # response._status_code = 301
    # response.headers['location'] = redirect_url + f"?email={user_name}"
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.autocorrect_location_header = False
    return response

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

@face_api_v1.route("/hello", methods=["GET"])
def hello():  
  response = make_response(
            jsonify({"username": "baoduy"}), 200)

  # response._status_code = 301
  # response.headers['location'] = "http://192.168.1.8:4000/" + f"?email=baoduy@gmail.com"
  # response.headers.add('Access-Control-Allow-Origin', '*')
  # response.autocorrect_location_header = False
  return response
  # return jsonify({"msg":f"Hello world" })

@face_api_v1.route("/delete_user", methods=["DELETE"])
def delete_face_label():
  if request.method == 'DELETE':        
    userName = request.form['username']    
    if userName:    
      isExits = find_by_username(userName)
      if isExits:
        delete_face(userName)          
        return jsonify({"msg":f"delete {userName} success" }), 200 
      return jsonify({"msg":f"{userName} not found" }), 400         
    else:
      return jsonify({"msg":f"{userName} is required" }), 400 

@face_api_v1.route("/get_faces_by_email", methods=["POST"])
def get_faces_by_user_name():
  if request.method == 'POST':        
    array_face_response = []
    userName = request.form['username']    
    if userName:    
      faces = get_faces_by_username(userName)
      for face in list(faces):        
        array_face_response.append({
          "label": face["label"],
          "face_embdding":face["face_embdding"]
        })
      # print(array_face_response)
      if faces:            
        return jsonify({"faces": array_face_response }), 200 
      return jsonify({"msg":f"{userName} not found" }), 400         
    else:
      return jsonify({"msg":f"{userName} is required" }), 400   


