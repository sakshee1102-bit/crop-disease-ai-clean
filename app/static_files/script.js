function uploadImage() {
    const input = document.getElementById("imageInput");
    const file = input.files[0];

    if (!file) {
        alert("Select image first");
        return;
    }

    document.getElementById("preview").src = URL.createObjectURL(file);

    const formData = new FormData();
    formData.append("image", file);

    fetch("/predict", {
    method: "POST",
    body: formData
})
.then(res => {
    if (!res.ok) throw new Error("Server error " + res.status);
    return res.json();
})
.then(data => {

    if (data.error) {
        alert(data.error);
        return;
    }

    // ✅ SAFETY DEFAULT
    const advice = data.advice || {
        symptoms: [],
        treatment: [],
        prevention: []
    };

    let html = `
        <h3>Disease: ${data.disease || "Unknown"}</h3>
        <p><b>Confidence:</b> ${data.confidence ?? "N/A"}%</p>

        <h4>Symptoms</h4>
        <ul>${advice.symptoms.map(i => `<li>${i}</li>`).join("") || "<li>Not available</li>"}</ul>

        <h4>Treatment</h4>
        <ul>${advice.treatment.map(i => `<li>${i}</li>`).join("") || "<li>Not available</li>"}</ul>

        <h4>Prevention</h4>
        <ul>${advice.prevention.map(i => `<li>${i}</li>`).join("") || "<li>Not available</li>"}</ul>
    `;

    document.getElementById("result").innerHTML = html;
})
.catch(err => {
    alert("Prediction failed. Please try again.");
    console.error(err);
});
