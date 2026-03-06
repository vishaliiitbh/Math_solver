import io
import base64
import os
from PIL import Image
import easyocr
import numpy as np

_reader = None

def get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    return _reader


def extract_text_from_image(image_bytes: bytes) -> dict:
    """
    Extract text from image bytes using EasyOCR.
    Returns dict with 'text', 'confidence', 'needs_hitl'.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(image)

        reader = get_reader()
        results = reader.readtext(img_array)

        if not results:
            return {
                "text": "",
                "confidence": 0.0,
                "needs_hitl": True,
                "raw_results": [],
                "error": "No text detected in image"
            }

        texts = []
        confidences = []
        for (bbox, text, confidence) in results:
            texts.append(text)
            confidences.append(confidence)

        combined_text = " ".join(texts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        needs_hitl = avg_confidence < 0.75

        return {
            "text": combined_text,
            "confidence": round(avg_confidence, 3),
            "needs_hitl": needs_hitl,
            "raw_results": results,
            "error": None
        }
    except Exception as e:
        return {
            "text": "",
            "confidence": 0.0,
            "needs_hitl": True,
            "raw_results": [],
            "error": str(e)
        }


def image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")
