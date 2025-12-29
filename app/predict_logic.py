import cv2
import numpy as np
import tensorflow as tf
import json

model = tf.keras.models.load_model("model/crop_disease_cnn.h5")

with open("model/class_labels.json", encoding="utf-8") as f:
    classes = json.load(f)

with open("advisory/disease_advisory.json", encoding="utf-8") as f:
    advisory = json.load(f)

def predict_disease(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)
    idx = int(np.argmax(pred))
    confidence = round(float(np.max(pred)) * 100, 2)

    disease = classes[idx]

    # ⚠️ VERY IMPORTANT: always return advice as object
    advice = advisory.get(disease, {
        "symptoms": ["No data available"],
        "treatment": ["No data available"],
        "prevention": ["No data available"]
    })

    return {
        "disease": disease,
        "confidence": confidence,
        "advice": advice
    }
