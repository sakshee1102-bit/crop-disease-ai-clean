import json

with open("advisory/disease_advisory.json") as f:
    advisory_data = json.load(f)

def get_advisory(disease_name):
    if disease_name in advisory_data:
        return advisory_data[disease_name]
    else:
        return "No advisory available"

# Example
disease = "Tomato_Late_blight"
info = get_advisory(disease)

print("\n🌾 Disease Advisory 🌾")
print("Disease:", info["disease"])
print("\nSymptoms:")
for s in info["symptoms"]:
    print("-", s)

print("\nTreatment:")
for t in info["treatment"]:
    print("-", t)

print("\nPrevention:")
for p in info["prevention"]:
    print("-", p)
