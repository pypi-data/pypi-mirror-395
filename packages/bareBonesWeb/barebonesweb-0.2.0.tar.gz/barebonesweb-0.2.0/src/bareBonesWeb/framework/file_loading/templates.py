import os
import asyncio
from ...__cache import __cached as _cache

def render_string(html: str, **context):
    """
    DISCLAIMER: This module does not use jinja
    __________________________________________
    Renders a html string using a custom rendering engine made by me
    """
    htmlSplitted = html.replace(r"{{", r"}}").split(r"}}")
    bracketsDone = 0
    for index, _ in enumerate(htmlSplitted.copy()):
        if index > 0:
            if index % 2 == 1:
                htmlSplitted.insert(index+bracketsDone, r"{{")
            else:
                htmlSplitted.insert(index+bracketsDone, r"}}")
            bracketsDone +=1

    doingCurlyBrackets = False
    for index, htmlSegment in enumerate(htmlSplitted.copy()):
        if htmlSegment == r"}}":
            doingCurlyBrackets = False
        if doingCurlyBrackets:
            exec("async def __insideBrackets():\n "+htmlSegment.replace("\n", "\n "), context)
            insideBrackets = context.get("__insideBrackets")
            async def main() -> list:
                bracketsResponse = insideBrackets()
                returnList: list[str] = []
                try:
                    returnList = [str(item) async for item in bracketsResponse]
                except:
                    pass
                returnList.append("")

                return returnList[:-1]
            htmlSplitted[index] = "".join(asyncio.run(main()))
        if htmlSegment == r"{{":
            doingCurlyBrackets = True

    return "".join(htmlSplitted).replace(r"{{", "").replace(r"}}", "")


def render_template(template: str, **context):
    """
    DISCLAIMER: This module does not use jinja
    __________________________________________
    Renders a file in the templates folder using a custom rendering engine made by me
    """

    templates_folder = _cache.get("templates_folder", None)
    if templates_folder:
        file_path = os.path.normpath(templates_folder+"/"+template)
        with open(file_path, "r") as file:
            returnVal = render_string(file.read(), **context)
        return returnVal
    else:
        raise LookupError("No application has been made yet")