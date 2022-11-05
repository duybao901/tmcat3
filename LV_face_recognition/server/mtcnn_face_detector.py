from numpy import asarray
from mtcnn.mtcnn import MTCNN
from PIL import Image # Pillow
import cv2


file = "./dataset/TRAIN_VN_20p_V1_6_8i/1/0.png"
# tải hình ảnh
image = Image.open(file)
# chuyển đổi sang RGB, nếu cần
image = image.convert('RGB')
# chuyển đổi sang array
pixels = asarray(image)    

detector = MTCNN()
# phát hiện khuôn mặt trong hình ảnh
results = detector.detect_faces(pixels)

for face in results:
    x,y,w,h = face['box']
    x1, y1, width, height = face['box']        
    x2, y2 = x1 + width, y1 + height

    # trích xuất khuôn mặt
    face = pixels[y1:y2, x1:x2]
    print(face)
    cv2.rectangle(pixels,(x,y),(x+w,y+h),(255,0,0),2)

cv2.imshow('img',pixels)
cv2.waitKey(0)
cv2.destroyAllWindows()