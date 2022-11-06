from keras.preprocessing.image import ImageDataGenerator
from numpy import asarray
from os import listdir
from os.path import isdir
from mtcnn.mtcnn import MTCNN

from PIL import Image # Pillow
import cv2

# trích xuất đặt trưng khuôn mặt từ file ảnh
# model facenet yêu cầu 160×160 pixels
# Using MTCNN
# tạo đối tượng mtcnn
detector = MTCNN()
def extract_face_mtcnn(filename, required_size=(224, 224)):
    print(filename)
    # tải hình ảnh
    image = Image.open(filename)
    # chuyển đổi sang RGB, nếu cần
    image = image.convert('RGB')
    # chuyển đổi sang array
    pixels = asarray(image)        
    # phát hiện khuôn mặt trong hình ảnh
    results = detector.detect_faces(pixels)
    if len(results) > 1 or results == []:
        return [];
    # trích xuất các giá trị toạ độ (bounding box) từ khuôn mặt 
    x1, y1, width, height = results[0]['box']
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height

    # trích xuất khuôn mặt
    face = pixels[y1:y2, x1:x2]
    
    # thay đổi kích thước pixel thành kích thước phù hợp với mô hình
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
def extract_face_haar(filename, required_size=(160, 160)):
    print(filename)
    # tải hình ảnh
    # tải hình ảnh
    image = Image.open(filename)
    # chuyển đổi sang RGB, nếu cần
    image = image.convert('RGB')
    # chuyển đổi sang array
    pixels = asarray(image) 
    # phát hiện khuôn mặt trong hình ảnh
    faces = face_cascade.detectMultiScale(pixels, 1.3,4)
    if len(faces) > 1 or faces == []:
        print("Heer")
        return  None;
    
    if len(faces) == 1:
        # print("FACES :::", faces)
        # trích xuất các giá trị toạ độ (bounding box) từ khuôn mặt 
        x1, y1, width, height = faces[0]    
        x1, y1 = abs(x1), abs(y1)   
        x2, y2 = x1 + width, y1 + height
        # trích xuất khuôn mặt
        face = pixels[y1:y2, x1:x2]
        # thay đổi kích thước pixel thành kích thước phù hợp với mô hình
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        return face_array

    if not all(faces):
        # print("FACES :::", faces)
        # trích xuất các giá trị toạ độ (bounding box) từ khuôn mặt 
        x1, y1, width, height = faces[0]   
        x1, y1 = abs(x1), abs(y1)     
        x2, y2 = x1 + width, y1 + height

        # trích xuất khuôn mặt
        face = pixels[y1:y2, x1:x2]
        # thay đổi kích thước pixel thành kích thước phù hợp với mô hình
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        print("face_array shape return",face_array.shape)
        return face_array
    

# tải hình ảnh và trích xuất khuôn mặt cho tất cả hình ảnh trong một thư mục
def load_faces(directory):
    faces = list()
    # liệt kê các ảnh
    for filename in listdir(directory):
        # path
        path = directory + "/" + filename
        # lấy khuôn mặt
        face = extract_face_mtcnn(path)	
        if face != [] and face is not None:
            faces.append(face)
    return faces     

# Tải thư mục chứa các thư mục con(label) chứa hình ảnh 
def load_dataset(directory):
    X, y = list(), list()
    # liệt kê các thư mục, trên mỗi lớp
    for subdir in listdir(directory):
        # path
        path = directory + "/" + subdir + '/'
        # Bỏ qua các phần tử không phải là thư mục
        if not isdir(path):
            continue
        print(path)
        # tải tất cả các khuôn mặt trong thư mục con
        faces = load_faces(path)
        # tạo nhãn
        labels = [subdir for _ in range(len(faces))]
        print("labels", labels)
        # tóm tắt tiến trình
        print('>loaded %d examples for class: %s' % (len(faces), subdir))
        # lưu
        X.extend(faces)
        y.extend(labels)
    return asarray(X), asarray(y)       

# Data
datagen = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)

datagen_tf = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    horizontal_flip=True)

# data = load_faces("./dataset/TRAIN_V8_100p_5i/Bao Dai")
