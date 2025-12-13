import socket
import os
from typing import Callable
from .framework import httpInteractions, forms
from .framework.forms import form
from .framework.file_loading.static import return_file_contents
from .framework.file_loading.templates import render_template, render_string
from.framework import urlTools
from .framework.urlTools import redirect
from .framework.database import *
from .framework.data_representation import charts
from . import __cache as _cache_mod
from .__cache import __cached as _cache
import sys
import threading
from io import BytesIO

class Application:
    request: httpInteractions.Request

    _module_path: str
    _templates_folder: str
    _static_folder: str
    _static_url_path: str
    _db_folder: str

    def __init__(self, module_name: str, templates_folder: str = "templates", static_folder: str = "static", static_url_path: str = "/static", database_folder: str = "database") -> None:
        self.urlMap = urlTools.urlMap()

        self._on_websocket_requests: list[Callable] = []

        self._module_name = module_name
        module_path = sys.modules[module_name].__file__
        if module_path:
            self._module_path = module_path
        else:
            raise ValueError("This is not a valid module_name")
        self._templates_folder = os.path.join(self._module_path, "..", templates_folder)
        self._static_folder = os.path.join(self._module_path, "..", static_folder)
        self._static_url_path = static_url_path
        self._db_folder = os.path.join(self._module_path, "..", database_folder)
        
        _cache_mod.__setattr__("templates_folder", self._templates_folder)
        _cache_mod.__setattr__("static_folder", self._static_folder)
        _cache_mod.__setattr__("static_url_path", self._static_url_path)
        _cache_mod.__setattr__("database_folder", self._db_folder)

    def add_url(self, URL: str, url_func: Callable, url_name: str | None = None):
        self.urlMap.add_url(urlTools.url(URL, url_func, url_name))

    def url(self, URL: str, url_name: str | None = None):
        def url_inner(f: Callable):
            self.add_url(URL, f, url_name)
            return f
        return url_inner
    
    def merge(self, app: Application, url_prefix: str | None = None):
        for url in app.urlMap.URLs.copy():
            if url_prefix:
                url.url = os.path.join(url_prefix, url.url)

            self.urlMap.add_url(url)

    def asWsgi(self, environ, start_response: Callable):
        """
        W.I.P NOT FINISHED - Use Application.run
        ----------------------------------------
        This used to make this app into a wsgi app that can be ran using a server e.g.
         -Gunicorn
         -Hypercorn
        """
        path = environ.get('PATH_INFO', '/')
        
        if self.urlMap.query("URL", path):
            content = self.urlMap.query("URL", path)() #type: ignore
            status = '200 OK'
        else:
            status = '404 Not Found'
            content = "404 Page not found"

        headers = [
            ("Content-Type", "text/html; charset=utf8"),
            ("Content-Length", str(len(content))),
        ]
        print("="*64)
        print(start_response.__code__.__repr__())
        print("="*64)
        start_response(status, headers)

        return [content.encode()]

    def handle_client(self, httpServer, client):
        global prev_snapshot
        snapshot = {}
        for root, _, files in os.walk(os.path.join(self._module_path, "..")):
            for file_name in files:
                full_path = os.path.join(root, file_name)

                if not (full_path.startswith(self._templates_folder) | full_path.startswith(self._static_folder)):
                    snapshot[full_path] = os.stat(full_path).st_mtime

        if prev_snapshot != snapshot:
            httpServer.close()
            print("\n")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        prev_snapshot = snapshot

        request_data_bytes = client.recv(1024)
        request_data = request_data_bytes.decode()

        stamp = os.stat

        try:
            headers_part, body_part = request_data.split('\r\n\r\n', 1)
        except ValueError:
            headers_part = request_data
            body_part = ""

        request_lines = headers_part.split("\r\n")

        if not request_lines:
            client.close()
            return
            
        try:
            method, path, ver = request_lines[0].split()
        except ValueError:
            client.close()
            return

        content_length = 0
        upgrade = ""
        websocket_key = ""

        for line in request_lines[1:]:
            if line.lower().startswith('content-length:'):
                content_length = int(line.split(': ')[1].strip())
                break
            if line.lower().startswith("upgrade:"):
                upgrade = line.split(': ')[1].strip()
            elif line.lower().startswith("sec-websocket-key:"):
                    websocket_key = line.split(': ')[1].strip()
            

        environ = {
            "REQUEST_METHOD": method,
            "SCRIPT_NAME": "",
            "PATH_INFO": path,
            "CONTENT_LENGTH": str(content_length),
            "SERVER_PROTOCOL": "HTTP/1.1",
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.input": BytesIO(body_part.encode('utf-8')),
            "upgrade": upgrade,
            "sec-websocket-key": websocket_key, 
        }

        self.request = httpInteractions.Request(environ)
        headers = [
        ["Content-Type:", "text/html; charset=utf8"],
        ]
        if environ["PATH_INFO"].endswith(".css"):
            headers[0][1] = "text/css; charset=utf8"
        if environ["PATH_INFO"].endswith(".js"):
            headers[0][1] = "text/javascript; charset=utf8"
        status, content = self.urlMap.exec_url(environ["PATH_INFO"])

        if isinstance(content, urlTools.redirect):
            status = content.code
            headers.append(["Location:", content.url])
            content = content()

        headers.append(["Content-Length:", str(len(content))])

        client.send(
            (f"HTTP/1.1 {status}\r\n"+
            "\r\n".join([" ".join(header) for header in headers])+
            "\r\n\r\n"+
            content)
            .encode()
        )

        print(f"\x1b[34mHTTP/1.1 \x1b[36m{status} \x1b[32m{environ["REQUEST_METHOD"]} \x1b[34m\"{environ["PATH_INFO"]}\"")

        client.shutdown(socket.SHUT_WR)
        client.close()

    def run(self, address: str = "localhost", port: int = 5000):
        self.address = address
        self.port = port

        #----------SETUP SOCKET----------#
        httpServer: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        httpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        httpServer.bind((address, port))
        httpServer.listen(5)

        print("\x1b[1m\x1b[35mThis is a development server. Do not use in production!\x1b[0m")
        print(f"\x1b[1m\x1b[34mListening on: {"http://"+httpServer.getsockname()[0]}:{port}\x1b[0m")

        #----------SOCKET LISTEN LOOP----------#
        global prev_snapshot
        prev_snapshot = {}
        for root, _, files in os.walk(os.path.join(self._module_path, "..")):
                for file_name in files:
                    full_path = os.path.join(root, file_name)
                    if not (full_path.startswith(self._templates_folder) | full_path.startswith(self._static_folder)):
                        prev_snapshot[full_path] = os.stat(full_path).st_mtime
        while(1):
            client, address = httpServer.accept()

            t = threading.Thread(target=self.handle_client, args=(httpServer, client))
            t.daemon = True
            t.start()