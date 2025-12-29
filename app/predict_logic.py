import os
import requests
import tensorflow as tf
import cv2
import numpy as np

MODEL_URL = "https://huggingface.co/sakshee1102/crop-disease-cnn/resolve/main/crop_disease_cnn.h5"
MODEL_PATH = "model/crop_disease_cnn.h5"

os.makedirs("model", exist_ok=True)

if not os.path.exists(MODEL_PATH):
    print("Downloading model from Hugging Face...")
    r = requests.get(MODEL_URL, timeout=120)
    with open(MODEL_PATH, "wb") as f:
        f.write(r.content)

print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded ✅")


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    return np.expand_dims(img, axis=0)


def predict_disease(image_path):
    img = preprocess_image(image_path)
    preds = model.predict(img)

    class_index = int(np.argmax(preds))
    confidence = float(np.max(preds)) * 100

    classes = ["Apple Scab", "Apple Black Rot", "Apple Cedar Rust", "Healthy"]

    return {
        "disease": classes[class_index],
        "confidence": round(confidence, 2),
        "advice": {
            "symptoms": ["Leaf spots"],
            "treatment": ["Use fungicide"],
            "prevention": ["Avoid excess moisture"]
        }
    }
