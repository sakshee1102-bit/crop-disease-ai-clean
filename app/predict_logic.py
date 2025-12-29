import os
import tensorflow as tf
import gdown

MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "crop_disease_cnn.h5")

MODEL_URL = "https://drive.google.com/uc?id=12JWffPZgJ8HOlc5Su3bwcsOHFw9hS60Z"

model = None  # do NOT load at import time


def load_model_once():
    global model
    if model is None:
        os.makedirs(MODEL_DIR, exist_ok=True)

        if not os.path.exists(MODEL_PATH):
            print("Downloading model from Google Drive...")
            gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

        print("Loading model...")
        model = tf.keras.models.load_model(MODEL_PATH)

    return model


def predict_disease(image_path):
    model = load_model_once()

    from tensorflow.keras.preprocessing import image
    import numpy as np

    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    preds = model.predict(x)

    return {
        "success": True,
        "prediction": preds.tolist()
    }
