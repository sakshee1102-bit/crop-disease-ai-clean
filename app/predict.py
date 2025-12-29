import cv2
import numpy as np
import tensorflow as tf
import json

model = tf.keras.models.load_model("model/crop_disease_cnn.h5")

with open("model/class_labels.json", encoding="utf-8") as f:
    classes = json.load(f)

img = cv2.imread("leaf.jpg")
img = cv2.resize(img, (224,224))
img = img / 255.0
img = np.expand_dims(img, axis=0)

pred = model.predict(img)
idx = np.argmax(pred)

print("Predicted Disease:", classes[idx])
print("Confidence:", round(float(np.max(pred))*100, 2), "%")
