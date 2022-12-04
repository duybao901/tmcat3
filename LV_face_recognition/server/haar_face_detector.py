import cv2
from PIL import Image # Pillow
from numpy import asarray

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# file = "./dataset/TRAIN_VN_500p_6_8i/1020/0.png"
file = "./face_test/Bao Duy/Bao Duy (1).jpg"

# tải hình ảnh
image = Image.open(file)
# chuyển đổi sang RGB, nếu cần
image = image.convert('RGB')
# chuyển đổi sang array
pixels = asarray(image) 

faces = face_cascade.detectMultiScale(pixels, 1.3,5)
print(faces)
if len(faces) > 1 or faces == []:
    print("A")
else:
    for face in faces:
        x,y,w,h = face
        x1, y1, width, height = face       
        x2, y2 = x1 + width, y1 + height
        # trích xuất khuôn mặt
        face = pixels[y1:y2, x1:x2]
        print(face)
        # trích xuất khuôn mặt
        face = pixels[y1:y2, x1:x2]
        cv2.rectangle(pixels,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.imshow('img',pixels)
    cv2.waitKey(0)
    cv2.destroyAllWindows()