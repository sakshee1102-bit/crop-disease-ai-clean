import os
import requests
import tensorflow as tf
import cv2
import numpy as np

MODEL_URL = "https://huggingface.co/sakshee1102/crop-disease-cnn/resolve/main/crop_disease_cnn.h5"
MODEL_PATH = "model/crop_disease_cnn.h5"

model = None

def load_model_once():
    global model

    if model is None:
        os.makedirs("model", exist_ok=True)

        if not os.path.exists(MODEL_PATH):
            print("Downloading model from Hugging Face...")
            r = requests.get(MODEL_URL, timeout=60)
            with open(MODEL_PATH, "wb") as f:
                f.write(r.content)

        model = tf.keras.models.load_model(MODEL_PATH)

    return model


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def predict_disease(image_path):
    model = load_model_once()

    img = preprocess_image(image_path)
    preds = model.predict(img)

    class_index = int(np.argmax(preds))
    confidence = float(np.max(preds)) * 100

    classes = [
        "Apple Scab",
        "Apple Black Rot",
        "Apple Cedar Rust",
        "Healthy"
    ]

    disease = classes[class_index]

    return {
        "disease": disease,
        "confidence": round(confidence, 2),
        "advice": {
            "symptoms": ["Leaf spots", "Color change"],
            "treatment": ["Use recommended fungicide"],
            "prevention": ["Crop rotation", "Avoid excess moisture"]
        }
    }
