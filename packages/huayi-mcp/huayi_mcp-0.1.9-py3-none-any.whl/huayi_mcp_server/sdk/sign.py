import hashlib
from urllib.parse import urlencode


def sign(secret: str, data: dict[str, str]) -> str:
    data_str = secret + urlencode(data) + secret
    return hashlib.md5(string=data_str.encode()).hexdigest()
