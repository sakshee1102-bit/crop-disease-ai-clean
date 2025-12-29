import cv2
import numpy as np
import tensorflow as tf
import json

# ===============================
# LOAD CNN MODEL
# ===============================
model = tf.keras.models.load_model("model/crop_disease_cnn.h5")

# ===============================
# LOAD CLASS LABELS
# ===============================
with open("model/class_labels.json", encoding="utf-8") as f:
    class_names = json.load(f)

# ===============================
# LOAD NLP ADVISORY (UTF-8 FIX)
# ===============================
with open("advisory/disease_advisory.json", encoding="utf-8") as f:
    advisory_data = json.load(f)

# ===============================
# LOAD IMAGE
# ===============================
IMAGE_PATH = "leaf.jpg"

img = cv2.imread(IMAGE_PATH)
if img is None:
    print("❌ Image not found! Put leaf.jpg in project root.")
    exit()

img = cv2.resize(img, (224, 224))
img = img / 255.0
img = np.expand_dims(img, axis=0)

# ===============================
# PREDICTION
# ===============================
prediction = model.predict(img)
index = int(np.argmax(prediction))
confidence = round(float(np.max(prediction)) * 100, 2)

disease = class_names[index]

print("\n✅ PREDICTION RESULT")
print("--------------------")
print("🦠 Disease :", disease)
print("📊 Confidence :", confidence, "%")

# ===============================
# NLP FARMER ADVISORY
# ===============================
print("\n🌾 FARMER ADVISORY")
print("--------------------")

if disease in advisory_data:
    info = advisory_data[disease]

    print("📌 Disease Name:", info["disease"])

    print("\n🔴 Symptoms:")
    for s in info["symptoms"]:
        print(" -", s)

    print("\n🧪 Treatment:")
    for t in info["treatment"]:
        print(" -", t)

    print("\n🛡 Prevention:")
    for p in info["prevention"]:
        print(" -", p)
else:
    print("⚠ Advisory data not available for this disease")
