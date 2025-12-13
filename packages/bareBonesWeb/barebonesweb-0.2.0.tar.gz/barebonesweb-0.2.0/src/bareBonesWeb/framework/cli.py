import sys
from typing import Callable

def cmd(cmd: str):
    def wrapper(f: Callable):
        if len(sys.argv) > 1 and sys.argv[1] == cmd:
            f()
            sys.exit()
        return f
    return wrapper