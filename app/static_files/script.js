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
        let html = `
            <h3>Disease: ${data.disease}</h3>
            <p><b>Confidence:</b> ${data.confidence}%</p>

            <h4>Symptoms</h4>
            <ul>${data.advice.symptoms.map(i => `<li>${i}</li>`).join("")}</ul>

            <h4>Treatment</h4>
            <ul>${data.advice.treatment.map(i => `<li>${i}</li>`).join("")}</ul>

            <h4>Prevention</h4>
            <ul>${data.advice.prevention.map(i => `<li>${i}</li>`).join("")}</ul>
        `;
        document.getElementById("result").innerHTML = html;
    })
    .catch(err => {
        alert(err.message);
        console.error(err);
    });
}
