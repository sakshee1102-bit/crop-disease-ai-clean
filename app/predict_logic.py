def predict_disease(image_path):
    if not HF_TOKEN:
        return {
            "error": "HF token not set",
            "advice": {"symptoms": [], "treatment": [], "prevention": []}
        }

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
                "advice": {"symptoms": [], "treatment": [], "prevention": []}
            }

        result = response.json()[0]

        return {
            "disease": result["label"],
            "confidence": round(result["score"] * 100, 2),
            "advice": {
                "symptoms": ["Leaf discoloration", "Spots on leaves"],
                "treatment": ["Use recommended fungicide"],
                "prevention": ["Avoid overwatering", "Use healthy seeds"]
            }
        }

    except Exception as e:
        return {
            "error": str(e),
            "advice": {"symptoms": [], "treatment": [], "prevention": []}
        }
