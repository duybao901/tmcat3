from os import listdir
from matplotlib import pyplot
from face_processing import extract_face

# load the photo and extract the face
folder = "./dataset/TRAIN_V2/Bao Anh/"
i = 1
# enumerate files
for filename in listdir(folder):  
  # path
  path = folder + filename
  # get face
  face = extract_face(path)
  if face is not None and i <= 15 and face != []: 
    print(i, face.shape)
    # plot
    pyplot.subplot(1, 6, i)
    pyplot.axis('off')
    pyplot.imshow(face)
    i += 1
  if i == 6:
    break

pyplot.show()
