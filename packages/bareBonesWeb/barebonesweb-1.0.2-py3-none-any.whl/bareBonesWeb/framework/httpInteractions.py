from .forms import formData

class Request:
    form: formData
    method: str
    url_scheme: str
    path: str
    protocol: str

    def __init__(self, environ: dict) -> None:
        content_length: int = int(environ["CONTENT_LENGTH"])
        form_data_bytes: bytes = environ["wsgi.input"].read(content_length)
        self.form = formData(form_data_bytes)
        self.method = environ["REQUEST_METHOD"]
        self.url_scheme = environ["wsgi.url_scheme"]
        self.path = environ["PATH_INFO"]
        self.protocal = environ["SERVER_PROTOCOL"]
    
    def __repr__(self) -> str:
        return f"Form: {self.form}"