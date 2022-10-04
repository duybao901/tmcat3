from keras.models import load_model

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Khoi tao model
def _load_model():
    facenet_keras_model = load_model("./models/facenet_keras.h5")
    return facenet_keras_model

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS