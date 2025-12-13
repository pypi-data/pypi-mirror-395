import sys
import bareBonesWeb

args = sys.argv

if args[1] == "docs":
    app = bareBonesWeb.Application(__name__)

    app.run()