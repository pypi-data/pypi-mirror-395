from typing import Any, Callable, Literal
from .file_loading.static import return_file_contents
from ..__cache import __cached as _cache
from pydoc import locate

class urlMap:
    URLs: list[url]

    def __init__(self) -> None:
        self.URLs = []

    def add_url(self, url: url):
        self.URLs.append(url)

    def query(self, query_by: Literal["URL", "url_func", "url_name"], value: str | Callable) -> url | None:
        for url in self.URLs:
            if query_by == "URL" and url.url == value:
                return url
            elif query_by == "url_func" and url.func == value:
                return url
            elif query_by == "url_name" and url.name == value:
                return url
        return None
    
    def exec_url(self, PATH_INFO: str):
            if PATH_INFO.startswith(_cache.get("static_url_path", "/static")):
                return ("200 OK", return_file_contents(PATH_INFO))
            
            clean_path = PATH_INFO.strip("/")
            path_segments = clean_path.split("/") if clean_path else []
            
            url_func = None
            kwargs = {}
            
            for url in self.URLs:
                clean_pattern = url.url.strip("/")
                pattern_segments = clean_pattern.split("/") if clean_pattern else []

                if len(pattern_segments) != len(path_segments):
                    continue
                
                match = True
                current_kwargs = {}
                
                for pat_seg, path_seg in zip(pattern_segments, path_segments):
                    if pat_seg.startswith("<") and pat_seg.endswith(">"):
                        try:
                            content = pat_seg[1:-1]
                            
                            if ":" in content:
                                name, type_str = content.split(":", 1)
                                name = name.strip()
                                type_str = type_str.strip()
                                
                                converter = locate(type_str)
                                if converter is None:
                                    raise ValueError(f"Unknown type: {type_str}")
                                
                                val = converter(path_seg)
                                current_kwargs[name] = val
                            else:
                                current_kwargs[content.strip()] = path_seg
                                
                        except Exception:
                            match = False
                            break
                    
                    elif pat_seg != path_seg:
                        match = False
                        break
                
                if match:
                    url_func = url.func
                    kwargs = current_kwargs
                    break

            if not url_func:
                return ("404 NOT FOUND", "404 Page Not Found")

            return ("200 OK", url_func(**kwargs))

class url:
    def __init__(self, URL: str, url_func: Callable, url_name: str | None = None) -> None:
        if URL == _cache.get("static_url_path"): raise ValueError("This value is already used for the static folder")
        if url_name:
            self.name = url_name
        else:
            self.name = url_func.__name__

        self.func = url_func
        self.url = URL

    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)

class redirect:
    def __init__(self, url: str, code: int = 302) -> None:
        self.url = url
        self.code = code

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return f"""
                <!DOCTYPE HTML>
                <html>
                    redirecting...
                    <br><br>
                    if not redirecting <a href='{self.url}'>click here</a>
                </html>
               """