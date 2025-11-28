from flask import Flask, render_template, request, jsonify
from embed_dwt import embed_watermark_dwt
import base64
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/watermark", methods=["POST"])
def watermark():
    file = request.files["image"]
    text = request.form["text"]
    alpha = float(request.form["alpha"])

    input_path = "temp_input.png"
    output_path = "temp_output.png"

    file.save(input_path)

    embed_watermark_dwt(input_path, text, output_path, alpha)

    with open(output_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return jsonify({"image": encoded})
from extract_dwt import extract_watermark_dwt

@app.route("/authenticate", methods=["POST"])
def authenticate():
    file = request.files["image"]
    input_path = "temp_auth.png"
    file.save(input_path)

    # Try extracting with reasonable max length
    extracted = extract_watermark_dwt(input_path, watermark_length=20)

    if extracted:
        return jsonify({"status": "valid", "message": extracted})
    else:
        return jsonify({"status": "invalid"})


if __name__ == "__main__":
    app.run(debug=True)
