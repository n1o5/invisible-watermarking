document.getElementById("applyBtn").onclick = async function () {
    let file = document.getElementById("imageInput").files[0];
    let text = document.getElementById("wmText").value;
    let alpha = document.getElementById("alpha").value / 100;

    if (!file) {
        alert("Please upload an image");
        return;
    }

    let formData = new FormData();
    formData.append("image", file);
    formData.append("text", text);
    formData.append("alpha", alpha);

    let res = await fetch("/watermark", {
        method: "POST",
        body: formData
    });

    let data = await res.json();

    let base64 = "data:image/png;base64," + data.image;

    document.getElementById("outputImage").src = base64;
    document.getElementById("downloadBtn").href = base64;

    document.getElementById("resultSection").classList.remove("hidden");
};
