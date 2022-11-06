from tensorflow import keras
import tensorflow as tf
from tensorflow.python.keras import backend as K
# from keras_vggface.vggface import VGGFace
# import keras_vggface


config = tf.compat.v1.ConfigProto(
    device_count={'GPU': 1},
    intra_op_parallelism_threads=1,
    allow_soft_placement=True
)
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.6
session = tf.compat.v1.Session(config=config)
K.set_session(session)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Khoi tao model
def _load_model():
    facenet_keras_model = keras.models.load_model("./models/facenet_self_train_triplot_500.h5", compile=False)
    return facenet_keras_model

_load_model()
# def _load_model_vggface2():
#     # check version of keras_vggface
#     # print version
#     print("keras_vggface.__version__ :",keras_vggface.__version__)
#     model = VGGFace(model='resnet50')
#     # summarize input and output shape
#     print('Inputs: %s' % model.inputs)
#     print('Outputs: %s' % model.outputs)
#     return model

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# _load_model_vggface2()