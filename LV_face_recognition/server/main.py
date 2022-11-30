import const
import pandas as pd
import KnnClass
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from KnnClass import KnnClass

Knn = KnnClass()
data = Knn.load_data_after_embedding(const.EMBDDINGS_FOLDER_EMB)

X_train, X_test, y_train, y_test = data['arr_0'], data['arr_1'], data['arr_2'], data['arr_3']

print('Dataset: train=%d, test=%d' % (X_train.shape[0], y_test.shape[0]))
print(X_train.shape)
print(X_test.shape)
print(X_train[0])
# print(X_test)
# print(y_test)

# normalize_input_vectors
X_train = Knn.normalize_input_vectors(X_train)
X_test = Knn.normalize_input_vectors(X_test)

print(X_train.shape)
print(X_test.shape)
# print(X_test)
# print(y_test)

# acc = 0.0
# for i in range(1,11):
#     print(f"With n_neighbors ={i}, weights='distance', p=2")
#     knn_model = KNeighborsClassifier(n_neighbors=i, weights='distance', p=2) 
#     knn_model.fit(X_train, y_train)

#     # predict
#     y_predict_train = knn_model.predict(X_train)
#     y_predict_test = knn_model.predict(X_test)

#     score_train = accuracy_score(y_train, y_predict_train)
#     score_test = accuracy_score(y_test, y_predict_test)
#     print('Accuracy: train=%.3f, test=%.3f \n' % (score_train, score_test))
#     acc += score_test

# print("\nAccuracy:::\n", acc/10)

# # summarize
# print('KNN Accuracy: train=%.3f, test=%.3f' % (score_train, score_test))

#df = pd.DataFrame(data= {"Y test": y_test, "Y predict test": y_predict_test})
#print(df)


# fit model
# svm_model = SVC(kernel='linear', probability=True)
# svm_model.fit(X_train, y_train )


# # predict
# y_predict_train = svm_model.predict(X_train)
# y_predict_test = svm_model.predict(X_test)

# score_train = accuracy_score(y_train, y_predict_train)
# score_test = accuracy_score(y_test, y_predict_test)

# # summarize
# print('SVM Accuracy: train=%.3f, test=%.3f' % (score_train, score_test))

# df = pd.DataFrame(data= {"Y train": y_predict_test, "Y test": y_test})
# print(df)