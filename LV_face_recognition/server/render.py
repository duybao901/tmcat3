from keras.models import load_model
import const
from face_processing import datagen, datagen_tf
import numpy as np
from KnnClass import KnnClass
########################################################################
model = load_model("./models/facenet_keras.h5")
Knn = KnnClass()
trainX, trainy = Knn.load_training_dataset(const.DATASET_FOLDER)
Knn.saving_traning_dataset_after_extract_feature(const.EMBDDINGS_FOLDER_EXT, trainX, trainy)


data = Knn.load_data_after_extract_feature(const.EMBDDINGS_FOLDER_EXT);
X_train, y_train = data["arr_0"], data["arr_1"]
print("trainX shape", X_train.shape)
print("trainy shape", y_train.shape)


X_train, X_test, y_train, y_test = Knn.split_data(X_train, y_train);

datagen.fit(X_train)
no_batch = 0
X_au = []
y_au = []
for i in np.arange(len(X_train)):
  no_img = 0
  for x in datagen.flow(np.expand_dims(X_train[i], axis = 0), batch_size = 1):
    X_au.append(x[0])
    y_au.append(y_train[i])
    no_img += 1
    if no_img == 6:
      break

datagen_tf.fit(X_test)

no_batch = 0
X_test_tf = []
for i in np.arange(len(X_test)):
  no_img = 0
  for x in datagen_tf.flow(np.expand_dims(X_test[i], axis = 0), batch_size = 1):
    X_test_tf.append(x[0])
    no_img += 1
    if no_img == 1:
      break


newTrainX = list()
for face_pixels in X_au:
  embedding = Knn.get_embedding(model, face_pixels)
  newTrainX.append(embedding)
newTrainX = np.asarray(newTrainX)
print(newTrainX.shape)

# convert each face in the test set to an embedding
newTestX = list()
for face_pixels in X_test_tf:
	embedding = Knn.get_embedding(model, face_pixels)
	newTestX.append(embedding)
newTestX = np.asarray(newTestX)
print(newTestX.shape)

Knn.save_data_after_embedding(const.EMBDDINGS_FOLDER_EMB ,newTrainX, newTestX , y_au, y_test)


#######################
# load dataset embddings from trainings files