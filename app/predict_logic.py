import os
import requests
import base64

HF_API_URL = "https://api-inference.huggingface.co/models/sakshee1102/crop-disease-cnn"
HF_TOKEN = os.environ.get("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

EMPTY_ADVICE = {
    "symptoms": [],
    "treatment": [],
    "prevention": []
}

def predict_disease(image_path):
    try:
        if not HF_TOKEN:
            return {
                "error": "HF token not configured",
                "advice": EMPTY_ADVICE
            }

        # read image
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        encoded = base64.b64encode(image_bytes).decode("utf-8")

        payload = {"inputs": encoded}

        response = requests.post(
            HF_API_URL,
            headers=HEADERS,
            json=payload,
            timeout=90
        )

        # HF error but still JSON-safe return
        if response.status_code != 200:
            return {
                "error": "Hugging Face inference failed",
                "details": response.text,
                "advice": EMPTY_ADVICE
            }

        data = response.json()

        # HF sometimes returns dict instead of list
        if isinstance(data, dict):
            return {
                "error": "Model is loading, try again in 10 seconds",
                "advice": EMPTY_ADVICE
            }

        result = data[0]

        return {
            "disease": result.get("label", "Unknown"),
            "confidence": round(result.get("score", 0) * 100, 2),
            "advice": {
                "symptoms": ["Leaf spots", "Discoloration"],
                "treatment": ["Apply recommended fungicide"],
                "prevention": ["Use disease-free seeds", "Avoid excess moisture"]
            }
        }

    except Exception as e:
        # 🔥 THIS PREVENTS 500 ERROR
        return {
            "error": "Internal prediction error",
            "details": str(e),
            "advice": EMPTY_ADVICE
        }
