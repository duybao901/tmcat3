from keras.preprocessing.image import ImageDataGenerator
from numpy import asarray
from os import listdir
from os.path import isdir
from mtcnn.mtcnn import MTCNN
from PIL import Image # Pillow


filename = "./face_test/Bui Tien Dung/Bui Tien Dung 1.jpg"
image = Image.open(filename)

image = Image.open(filename)
    # chuyển đổi sang RGB, nếu cần
image = image.convert('RGB')
# chuyển đổi sang array
pixels = asarray(image)  

detector = MTCNN()
# phát hiện khuôn mặt trong hình ảnh
results = detector.detect_faces(pixels)


print(results[0]['box'])