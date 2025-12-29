import os
import json

TRAIN_DIR = "dataset/train"
OUTPUT_FILE = "model/class_labels.json"

# Get class names
class_names = sorted([
    d for d in os.listdir(TRAIN_DIR)
    if os.path.isdir(os.path.join(TRAIN_DIR, d))
])

# Save to json
os.makedirs("model", exist_ok=True)
with open(OUTPUT_FILE, "w") as f:
    json.dump(class_names, f, indent=2)

print("✅ class_labels.json created successfully")
print("Classes:", class_names)
