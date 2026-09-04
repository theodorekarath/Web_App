# Handwritten Digit Recognizer Web App

A minimal Flask website for drawing a handwritten digit and receiving a model
prediction with a confidence score. It is independent of the Tkinter project:
the CNN architecture, preprocessing, inference code, and best model checkpoint
are contained in this folder.

## Run locally

```bash
python3 -m venv venv-web
source venv-web/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python webapp.py
```

Open <http://127.0.0.1:5000>.

The app loads `BEST_MODEL.pth`, falling back to `TRAINED_MODEL.pth` if present.
Use **Predict** after drawing and **Clear** to reset the canvas.

## Browser test

With the server running in one terminal:

```bash
python -m playwright install chromium
python playwright_check.py
```
