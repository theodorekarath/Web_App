from PIL import Image
from torchvision import transforms


transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])


def prepare_drawing(image, content_size=20):
    """Crop, scale, and center a browser drawing for MNIST-style inference."""
    if image.mode != "L":
        image = image.convert("L")
    bbox = image.getbbox()
    if bbox is None:
        return Image.new("L", (28, 28), 0)

    digit = image.crop(bbox)
    scale = content_size / max(digit.size)
    resized_size = tuple(max(1, round(side * scale)) for side in digit.size)
    digit = digit.resize(resized_size, Image.Resampling.LANCZOS)

    canvas = Image.new("L", (28, 28), 0)
    canvas.paste(digit, ((28 - digit.width) // 2, (28 - digit.height) // 2))
    return canvas
