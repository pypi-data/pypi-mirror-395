from typing import Any

def pg_not_fnd():
    return "<h1>404 Page Not Found</h1>"

__cached: dict[str, Any] = {"404_page": pg_not_fnd}

def __setattr__(name: str, value):
    __cached[name] = value