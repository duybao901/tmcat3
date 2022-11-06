# USING_DATASET = "A"
USING_DATASET = "TRAIN_VN_100p_6_8i"

# DATASET_FOLDER = "./dataset/" + USING_DATASET
# EMBDDINGS_FOLDER_EXT = "./embeddings/" + USING_DATASET + "_ext.npz"
# EMBDDINGS_FOLDER_EMB = "./embeddings/" + USING_DATASET + "_emb.npz"

DATASET_FOLDER = "./dataset/" + USING_DATASET
EMBDDINGS_FOLDER_EXT = "./embeddings/facenet/" + "TRAIN_VN_100p_6_8i_6g_mtcnn_v1_triplot_500" + "_ext.npz"
EMBDDINGS_FOLDER_EMB = "./embeddings/facenet/" + "TRAIN_VN_100p_6_8i_6g_mtcnn_v1_triplot_500" + "_emb.npz"


import keras; 
print("keras version", keras.__version__)
import tensorflow as tf
print("tensorflow version",tf.__version__)

