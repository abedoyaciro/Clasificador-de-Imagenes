import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model

# Modelo cargado una vez al inicio
base_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
modelo_visual = Model(inputs=base_model.input, outputs=base_model.output)


def extraer_embedding_visual(path_img):
    """
    Extrae un embedding visual general (cuerpo, ropa, fondo) de la
    imagen completa.
    """
    img = image.load_img(path_img, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = modelo_visual.predict(x)
    return features.flatten()
