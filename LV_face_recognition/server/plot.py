from os import listdir
from matplotlib import pyplot
from face_processing import extract_face
from face_processing import datagen, datagen_tf, load_faces
import numpy as np
from numpy import asarray
# load the photo and extract the face
folder = "./face_test/Le Duy/"

# enumerate files
# for filename in listdir(folder):  
#   # path
#   path = folder + filename
#   # get face
#   face = extract_face(path)
#   if face is not None and i <= 15 and face != []: 
#     print(i, face.shape)
#     # plot
#     pyplot.subplot(1, 6, i)
#     pyplot.axis('off')
#     pyplot.imshow(face)
#     i += 1
#   if i == 6:
#     break


face_array = load_faces(folder)


print(face_array)

datagen.fit(asarray(face_array))
no_batch = 0
face_datagen = []
for i in np.arange(len(face_array)):
  no_img = 0
  for x in datagen.flow(np.expand_dims(face_array[i], axis = 0), batch_size = 1):
    face_datagen.append(x[0])
    no_img += 1
    if no_img == 6:
      break

i = 1
for face in face_datagen:
  if face is not None and face != []:     
    # print(i, face_datagen.shape)
    # plot
    pyplot.subplot(4, 8, i)
    pyplot.axis('off')
    pyplot.imshow(face)
    i += 1
    if i == len(face_datagen):
      break

pyplot.show()

# face_array = load_faces(folder)
# face_a = []
# image = face_array[0]
# face_a.append(image)
# datagen_tf.fit([image])
# face_datagen = []
# X =  datagen_tf.flow(np.expand_dims(image, axis = 0), batch_size = 1)
# # pyplot.imshow(X[0][0])
# face_a.append(X[0][0])

# i = 1
# for face in face_a:
#   if face is not None and face != []:     
#     # print(i, face_datagen.shape)
#     # plot
#     pyplot.subplot(2, 2, i)
#     pyplot.axis('off')
#     pyplot.imshow(face)
#     i += 1
#     if i == len(face_a) + 1:
#       break

# pyplot.show()