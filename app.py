import os

from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/output/result"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files:
        return "No file uploaded"

    file = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Run YOLO detection
    os.system(
        f'python detect.py --weights runs/train/exp10/weights/best.pt --source "{filepath}" --project static/output --name result --exist-ok'
    )

    return render_template("index.html", result_image=f"static/output/result/{file.filename}")


if __name__ == "__main__":
    app.run(debug=True)
