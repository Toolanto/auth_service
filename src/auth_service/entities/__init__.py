import base64

def encode(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode('utf-8')
    