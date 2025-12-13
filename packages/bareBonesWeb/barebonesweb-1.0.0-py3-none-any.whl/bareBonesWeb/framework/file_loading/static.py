import os
from ...__cache import __cached as _cache

def return_file_contents(PATH_INFO: str):
    static_folder: str = _cache["static_folder"]
    static_url_path: str = _cache["static_url_path"]
    PATH_INFO = PATH_INFO.removeprefix(static_url_path)
    
    file_path = os.path.normpath(static_folder+"/"+PATH_INFO)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    else:
        return ""