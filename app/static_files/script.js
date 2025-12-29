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

    fetch("https://crop-disease-ai-clean.onrender.com/predict", {

        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {

        console.log("Response:", data); // MUST PRINT

        if (data.error) {
            alert(data.error);
            return;
        }

        let result = `
            <h3>Disease: ${data.disease}</h3>
            <p><b>Confidence:</b> ${data.confidence}%</p>
        `;

        result += "<h4>Symptoms</h4><ul>";
        (data.advice.symptoms || []).forEach(i => result += `<li>${i}</li>`);
        result += "</ul>";

        result += "<h4>Treatment</h4><ul>";
        (data.advice.treatment || []).forEach(i => result += `<li>${i}</li>`);
        result += "</ul>";

        result += "<h4>Prevention</h4><ul>";
        (data.advice.prevention || []).forEach(i => result += `<li>${i}</li>`);
        result += "</ul>";

        document.getElementById("result").innerHTML = result;
    })
    .catch(err => {
        console.error(err);
        alert("Backend connection failed");
    });
}
