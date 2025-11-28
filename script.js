// =====================
// EMBEDDING (LEFT SIDE)
// =====================

document.getElementById("applyBtn").onclick = async function () {

    let file = document.getElementById("imageInput").files[0];
    let text = document.getElementById("wmText").value.trim();
    let alpha = document.getElementById("alpha").value / 100;

    let errorBox = document.getElementById("embedError");
    let embedCard = document.getElementById("embedCard");

    // Reset errors
    errorBox.classList.add("hidden");
    errorBox.textContent = "";

    // Validate
    if (!file) {
        errorBox.textContent = "Please upload an image to embed the watermark.";
        errorBox.classList.remove("hidden");
        embedCard.classList.add("shake");
        setTimeout(() => embedCard.classList.remove("shake"), 400);
        return;
    }

    if (text === "") {
        errorBox.textContent = "Please enter the watermark text.";
        errorBox.classList.remove("hidden");
        embedCard.classList.add("shake");
        setTimeout(() => embedCard.classList.remove("shake"), 400);
        return;
    }

    // Prepare data
    let formData = new FormData();
    formData.append("image", file);
    formData.append("text", text);
    formData.append("alpha", alpha);

    // Call backend
    let res = await fetch("/watermark", {
        method: "POST",
        body: formData
    });

    let data = await res.json();
    let base64 = "data:image/png;base64," + data.image;

    // Display output
    document.getElementById("outputImage").src = base64;
    document.getElementById("downloadBtn").href = base64;
    document.getElementById("resultSection").classList.remove("hidden");
};



// ==========================
// AUTHENTICATION (RIGHT SIDE)
// ==========================

document.getElementById("authBtn").onclick = async function () {

    let file = document.getElementById("authImage").files[0];
    let errorBox = document.getElementById("authError");
    let authCard = document.getElementById("authCard");

    // Reset errors
    errorBox.classList.add("hidden");
    errorBox.textContent = "";

    if (!file) {
        errorBox.textContent = "Please upload a watermarked image.";
        errorBox.classList.remove("hidden");
        authCard.classList.add("shake");
        setTimeout(() => authCard.classList.remove("shake"), 400);
        return;
    }

    let formData = new FormData();
    formData.append("image", file);

    let res = await fetch("/authenticate", {
        method: "POST",
        body: formData
    });

    let data = await res.json();

    // Hide info block
    document.getElementById("authInfo").style.display = "none";

    let resultBox = document.getElementById("authResult");

    if (data.status === "valid") {
        resultBox.textContent = "Watermark Valid: " + data.message;
        resultBox.className = "text-green-400 text-center text-lg font-semibold";
    } else {
        resultBox.textContent = "No valid watermark found";
        resultBox.className = "text-red-400 text-center text-lg font-semibold";
    }
};
