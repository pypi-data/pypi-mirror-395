class SDK(object):
    def __init__(self, base_url: str, secret: str, **kwargs: object) -> None:
        self.base_url: str = base_url
        self.secret: str = secret
        self.headers: dict[str, str] = {"Content-Type": "application/json"}
