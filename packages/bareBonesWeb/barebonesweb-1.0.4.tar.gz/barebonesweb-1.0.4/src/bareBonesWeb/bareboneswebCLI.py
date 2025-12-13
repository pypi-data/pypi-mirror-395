import sys
from bareBonesWeb import Application

def cli():
    args = sys.argv

    if len(args) > 1:
        if args[1] == "docs":
            app = Application(__name__)

            app.run()

cli()