from base64 import b64encode
from io import BytesIO

from PIL import Image

import webapp


def png_data_url(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return "data:image/png;base64," + b64encode(buffer.getvalue()).decode()


def test_index_loads():
    response = webapp.create_app().test_client().get("/")
    assert response.status_code == 200
    assert b"drawing-canvas" in response.data


def test_predict_uses_shared_inference(monkeypatch):
    app = webapp.create_app()
    monkeypatch.setattr(webapp, "load_model", lambda: None)
    monkeypatch.setattr(webapp, "predict_from_image", lambda image: (7, 98.765))
    image = Image.new("L", (700, 700), 0)
    image.paste(255, (300, 200, 400, 500))

    response = app.test_client().post("/predict", json={"image": png_data_url(image)})
    assert response.status_code == 200
    assert response.get_json() == {"digit": 7, "confidence": 98.77, "confident": True}


def test_predict_rejects_blank_canvas():
    image = Image.new("L", (700, 700), 0)
    response = webapp.create_app().test_client().post("/predict", json={"image": png_data_url(image)})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Draw a digit before predicting."
