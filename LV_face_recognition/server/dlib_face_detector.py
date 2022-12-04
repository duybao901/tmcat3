import cv2
from PIL import Image # Pillow
from numpy import asarray
import dlib

# https://pyimagesearch.com/2021/04/19/face-detection-with-dlib-hog-and-cnn/
# Thư viện dlib được cho là một trong những gói được sử dụng nhiều nhất để nhận dạng khuôn mặt. 
# Một gói Python được đặt tên thích hợp face_recognition kết hợp các chức năng nhận dạng khuôn 
# mặt của dlib thành một API đơn giản, dễ sử dụng.

def convert_and_trim_bb(image, rect):
    # extract the starting and ending (x, y)-coordinates of the
    # bounding box
    startX = rect.left()
    startY = rect.top()
    endX = rect.right()
    endY = rect.bottom()
    # ensure the bounding box coordinates fall within the spatial
    # dimensions of the image
    startX = max(0, startX)
    startY = max(0, startY)
    endX = min(endX, image.shape[1])
    endY = min(endY, image.shape[0])
    # compute the width and height of the bounding box
    w = endX - startX
    h = endY - startY
    # return our bounding box coordinates
    return (startX, startY, w, h)

# load dlib's HOG + Linear SVM face detector
print("[INFO] loading HOG + Linear SVM face detector...")
detector = dlib.get_frontal_face_detector()

# file = "./dataset/TRAIN_VN_500p_6_8i/1020/1.png"
file = "./face_test/Unknow/psg_team_1.jpg"


# tải hình ảnh
# image = Image.open(file)
# # chuyển đổi sang RGB, nếu cần
# image = image.convert('RGB')
# # chuyển đổi sang array
# pixels = asarray(image) 

# rects = detector(pixels)
# print(rects)

# boxes = [convert_and_trim_bb(pixels, r) for r in rects]
# # loop over the bounding boxes
# for (x, y, w, h) in boxes:
# 	# draw the bounding box on our image
# 	cv2.rectangle(pixels, (x, y), (x + w, y + h), (255, 0, 0), 2)
# # show the output image
# cv2.imshow("Output", pixels)
# cv2.waitKey(0)