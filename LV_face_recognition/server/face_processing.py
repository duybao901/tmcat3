from tensorflow.keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot
from numpy import asarray
from os import listdir
from os.path import isdir
from mtcnn.mtcnn import MTCNN
import cv2

from PIL import Image # Pillow

# extract faces in filename image
def extract_face(filename, required_size=(160, 160)):
    print(filename)
    # load image from file
    image = Image.open(filename)
    # convert to RGB, if needed
    image = image.convert('RGB')
    # convert to array
    pixels = asarray(image)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    results = detector.detect_faces(pixels)

    if len(results) > 1 or results == []:
        return [];

    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    # bug fix
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array

# load images and extract faces for all images in a directory
def load_faces(directory):
    faces = list()
  # enumerate files
    for filename in listdir(directory):
    # path
        path = directory + "/" + filename
        # get face
        face = extract_face(path)	
        		 
        if face != []:
            faces.append(face)
    return faces     

# load a dataset that contains one subdir for each class that in turn contains images
def load_dataset(directory):
    X, y = list(), list()
    # enumerate folders, on per class
    for subdir in listdir(directory):
        # path
        path = directory + "/" + subdir + '/'
        # skip any files that might be in the dir
        if not isdir(path):
            continue
        print(path)
        # load all faces in the subdirectory
        faces = load_faces(path)
        # create labels
        labels = [subdir for _ in range(len(faces))]
        print(labels)
        # summarize progress
        print('>loaded %d examples for class: %s' % (len(faces), subdir))
        # store
        X.extend(faces)
        y.extend(labels)
    return asarray(X), asarray(y)       


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
    rotation_range=20,
    # width_shift_range=0.2,
    # height_shift_range=0.2,
    horizontal_flip=True)

# data = load_faces("./dataset/TRAIN_V8_100p_5i/Bao Dai")
