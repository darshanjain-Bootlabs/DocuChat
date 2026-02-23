import easyocr
from pathlib import Path

def text_from_image(image_path: Path) -> str:
    reader = easyocr.Reader(['en'])
    result = reader.readtext(str(image_path))
    return "\n".join([text for (_, text, _) in result])