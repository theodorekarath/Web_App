from pathlib import Path

import torch

from config import BEST_CHECKPOINT_PATH, CHECKPOINT_PATH
from model import Net
from preprocessing import prepare_drawing, transform


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Net().to(device)


def load_model(model_path=None):
    if model_path is None:
        model_path = BEST_CHECKPOINT_PATH if BEST_CHECKPOINT_PATH.exists() else CHECKPOINT_PATH
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"{model_path} not found. Add a trained checkpoint first.")
    try:
        checkpoint = torch.load(model_path, map_location=device, weights_only=True)
    except TypeError:
        checkpoint = torch.load(model_path, map_location=device)

    state_dict = checkpoint["model_state"] if isinstance(checkpoint, dict) and "model_state" in checkpoint else checkpoint
    model.load_state_dict(state_dict)
    model.eval()
    return model


def predict_from_image(image):
    image = prepare_drawing(image)
    image_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        probabilities = torch.softmax(model(image_tensor), dim=1)
        confidence, prediction = torch.max(probabilities, dim=1)
    return prediction.item(), confidence.item() * 100
