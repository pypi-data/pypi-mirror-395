import base64


def base64_decode(value: str) -> str:
    return base64.b64decode(value).replace(b'\x00', b'').decode('utf-8', errors='replace')


def base64_encode(value: str) -> str:
    return base64.b64encode(value.encode('utf-8')).decode('ascii')
