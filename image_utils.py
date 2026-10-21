import base64
import io
from PIL import Image


def image_to_data_url(uploaded_file, max_side=1024):
    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((max_side, max_side))   # garde les proportions

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)

    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"