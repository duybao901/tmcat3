import tensorflow as tf
from tensorflow.keras.layers import Dense, Lambda, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import VGG16
import tensorflow_addons as tfa
from keras.utils import np_utils
from sklearn import preprocessing

from KnnClass import KnnClass
Knn = KnnClass()
import const
from PIL import Image

def _base_network():
    model = VGG16(include_top = True, weights = None)
    dense = Dense(128)(model.layers[-4].output)
    norm2 = Lambda(lambda x: tf.math.l2_normalize(x, axis = 1))(dense)
    model = Model(inputs = [model.input], outputs = [norm2])
    return model

model = _base_network()
model.summary()

data = Knn.load_data_after_extract_feature(const.EMBDDINGS_FOLDER_EXT);
X_train, y_train = data["arr_0"], data["arr_1"]
print("trainX shape", X_train.shape)
print("trainy shape", y_train.shape)
X_train, X_test, y_train, y_test = Knn.split_data(X_train, y_train)
print(X_train.shape)
print(X_test.shape)

label_encoder = preprocessing.LabelEncoder()
y_train = label_encoder.fit_transform(y_train)
y_test = label_encoder.fit_transform(y_test)

model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=tfa.losses.TripletSemiHardLoss())

gen_train = tf.data.Dataset.from_tensor_slices((X_train, y_train)).repeat().shuffle(1024).batch(32)
print(gen_train)

history = model.fit(
    gen_train,
    steps_per_epoch = 50,
    epochs=10)

model.save("./models/facenet_model_triplot.h5")