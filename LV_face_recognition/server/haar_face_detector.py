import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

img = cv2.imread("./face_test/Bui Tien Dung/Bui Tien Dung 1.jpg")
faces = face_cascade.detectMultiScale(img, 1.1,4)
print(faces)