import os
import requests
import base64

HF_API_URL = "https://api-inference.huggingface.co/models/sakshee1102/crop-disease-cnn"
HF_TOKEN = os.environ.get("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def predict_disease(image_path):
    if not HF_TOKEN:
        return {"error": "HF token not set"}

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    encoded = base64.b64encode(image_bytes).decode("utf-8")

    payload = {"inputs": encoded}

    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return {
                "error": "Inference failed",
                "status": response.status_code,
                "details": response.text
            }

        result = response.json()[0]

        return {
            "disease": result["label"],
            "confidence": round(result["score"] * 100, 2),
            "advice": {
                "symptoms": [],
                "treatment": [],
                "prevention": []
            }
        }

    except Exception as e:
        return {"error": str(e)}
