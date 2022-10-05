import numpy as np
from numpy import load, savez_compressed, expand_dims
from keras.models import load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from face_processing import load_dataset

class KnnClass:    
    def myweight(self, distances):
        sigma2 = .5 # we can change this number
        return np.exp(-distances**2/sigma2)

    def fit_model(self, X_train, y_train):
        self.clf.fit(X_train, y_train)

    # load dataset
    def load_training_dataset(self, DATASET_FOLDER):
        trainX, trainy = load_dataset(DATASET_FOLDER)
        return trainX, trainy
    
    def saving_traning_dataset_after_extract_feature(self, folder, X_train, y_train):
        savez_compressed(folder, X_train, y_train)
        print("Save sucess", folder)
    
    # load the face dataset after extract feature 
    def load_data_after_extract_feature(self, folder):
        data = load(folder, allow_pickle=True)
        return data
    
    def split_data(self, X_train, y_train):
        X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, train_size=0.8, test_size=0.2, random_state=1)
        return X_train, X_test, y_train, y_test

    # calculate a face embedding for each face in the dataset using facenet
    def get_embedding(self, model, face_pixels):        
        # scale pixel values
        face_pixels = face_pixels.astype('float32')
        # standardize pixel values across channels (global)
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        # transform face into one sample
        samples = expand_dims(face_pixels, axis=0)
        # make prediction to get embedding
        yhat = model.predict(samples)
        return yhat[0]

    def save_data_after_embedding(self, folder, newTrainX,newTestX , y_train, y_test):
        savez_compressed(folder, newTrainX, newTestX, y_train, y_test)
        print("Save sucess", folder)

    def load_data_after_embedding(self, folder):
        data = load(folder, allow_pickle=True)  
        return data

    def normalize_input_vectors(self, vector):
        in_encoder = Normalizer(norm='l2')
        vector = in_encoder.transform(vector)
        return vector

