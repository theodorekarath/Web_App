"""Minimal Flask interface for the handwritten digit recognizer."""

from base64 import b64decode
from binascii import Error as Base64Error
from io import BytesIO
from threading import Lock

from flask import Flask, jsonify, render_template, request
from PIL import Image, UnidentifiedImageError

from config import CONFIDENCE_THRESHOLD
from inference import load_model, predict_from_image


MAX_IMAGE_BYTES = 2 * 1024 * 1024


def create_app():
    app = Flask(__name__)
    model_lock = Lock()
    app.config["MODEL_LOADED"] = False

    def ensure_model_loaded():
        if not app.config["MODEL_LOADED"]:
            with model_lock:
                if not app.config["MODEL_LOADED"]:
                    load_model()
                    app.config["MODEL_LOADED"] = True

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/predict")
    def predict():
        image_data = (request.get_json(silent=True) or {}).get("image")
        if not isinstance(image_data, str) or not image_data.startswith("data:image/png;base64,"):
            return jsonify(error="Please submit a PNG drawing."), 400
        try:
            raw_image = b64decode(image_data.split(",", 1)[1], validate=True)
        except (IndexError, Base64Error):
            return jsonify(error="The drawing could not be read."), 400
        if len(raw_image) > MAX_IMAGE_BYTES:
            return jsonify(error="The drawing is too large."), 413
        try:
            with Image.open(BytesIO(raw_image)) as source:
                image = source.convert("L")
        except (UnidentifiedImageError, OSError):
            return jsonify(error="The drawing could not be read."), 400
        if image.getbbox() is None:
            return jsonify(error="Draw a digit before predicting."), 400
        try:
            ensure_model_loaded()
            digit, confidence = predict_from_image(image)
        except FileNotFoundError as error:
            return jsonify(error=str(error)), 503
        return jsonify(digit=digit, confidence=round(confidence, 2), confident=confidence >= CONFIDENCE_THRESHOLD)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
