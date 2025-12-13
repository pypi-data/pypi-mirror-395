import sys
import bareBonesWeb

def cli():
    args = sys.argv

    if args[0] == "docs":
        app = bareBonesWeb.Application(__name__)

        app.run()