function uploadImage() {
    let input = document.getElementById("imageInput");
    let file = input.files[0];

    if (!file) {
        alert("Please select image");
        return;
    }

    // Image preview
    document.getElementById("preview").src = URL.createObjectURL(file);

    let formData = new FormData();
    formData.append("image", file);

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Backend response:", data); // 🔍 DEBUG

        let resultDiv = document.getElementById("result");

        let html = `
            <h3>🦠 Disease: ${data.disease}</h3>
            <p><b>Confidence:</b> ${data.confidence}%</p>
        `;

        html += "<h4>🔴 Symptoms</h4><ul>";
        data.advice.symptoms.forEach(s => html += `<li>${s}</li>`);
        html += "</ul>";

        html += "<h4>🧪 Treatment</h4><ul>";
        data.advice.treatment.forEach(t => html += `<li>${t}</li>`);
        html += "</ul>";

        html += "<h4>🛡 Prevention</h4><ul>";
        data.advice.prevention.forEach(p => html += `<li>${p}</li>`);
        html += "</ul>";

        resultDiv.innerHTML = html;
    })
    .catch(err => {
        console.error("Error:", err);
        alert("Prediction failed");
    });
}
