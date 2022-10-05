from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import os

datagen = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)

for subDir in os.listdir("./dataset/TRAIN_V1_5p_1_image"):
    print("subDir", subDir)
    for image in os.listdir("./dataset/TRAIN_V1_5p_1_image" + "/" + subDir):
        image_path = "./dataset/TRAIN_V1_5p_1_image" + "/" + subDir + "/" + image
        pic = load_img(image_path)
        pic_array = img_to_array(pic)
        pic_array = pic_array.reshape((1,) + pic_array.shape) # Converting into 4 dimension array
        count = 1
        for batch in datagen.flow(pic_array, batch_size=5, save_to_dir="./image_generator/TRAIN_V1_5p_1_image" + "/" + subDir, save_prefix=subDir, save_format='jpeg'):
            count += 1
            if count >= 15:
                break



# pic = load_img("./dataset/TRAIN_V1_5p_1_image/Bae Suzy/BaeSuzy (1).jpeg")
# pic_array = img_to_array(pic)
# print(pic_array.shape)

# pic_array = pic_array.reshape((1,) + pic_array.shape) # Converting into 4 dimension array
# print(pic_array.shape)


# # Generate 10 images
# # batch_size: At a time, how many image should be created.
# 
# for batch in datagen.flow(pic_array, batch_size=5, save_to_dir="image_dataset/generated_image", save_prefix='dog', save_format='jpeg'):
#     count += 1
#     if count > 10:
#         break