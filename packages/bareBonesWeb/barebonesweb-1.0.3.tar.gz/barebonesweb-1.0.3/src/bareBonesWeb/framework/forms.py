from typing import Any, Literal

class formData:
    rawDict: dict[str, str]

    _decode_table = {r"%2F": "/",
     r"%5C": "\\",
     r"%3D": "=",
     "+": " ",
     r"%2B": "+",
     r"%26": "&"}

    def __init__(self, formBytes: bytes) -> None:
        self.rawDict = {}
        rawString: str = formBytes.decode()
        rawList: list[str] = rawString.split("&")
        for listItem in rawList:
            splittedItem = listItem.split("=")
            if splittedItem[0]:
                try:
                    value = splittedItem[1]
                except:
                    value = ""
                self.rawDict[splittedItem[0]] = value


    def __getitem__(self, key: str):
        returnVal: str = self.rawDict[key]
        for encoded, decoded in self._decode_table.items():
            returnVal = returnVal.replace(encoded, decoded)
        return returnVal
    def get(self, key: str, default):
        try: self.__getitem__(key)
        except: return default

    def __str__(self) -> str:
        returnVal = self.rawDict.__str__()
        for encoded, decoded in self._decode_table.items():
            returnVal = returnVal.replace(encoded, decoded)
        return returnVal
    
class form:
    id: str
    inputs: list[str]

    def __init__(self, form_name: str) -> None:
        self.inputs = []
        self.id = form_name

    def add_input(self, input_type: Literal["button", "checkbox", "color", "date", "datetime-local", "email", "file", "hidden", "image", "month", "number", "password", "range", "reset", "search", "tel", "text", "time", "url", "week"], value: str | None = None, placeholder: str | None = None):
        self.inputs.append(f"<input type='{input_type}' {"value='"+value+"'" if value else ""} {"placeholder='"+placeholder+"'" if placeholder else ""}>")

    def __call__(self, method: Literal["GET", "POST"] = "POST") -> Any:
        return f"""
                <fieldset>
                    <legend>{self.id}</legend>
                    <form method='{method}' id='{self.id}'>
                        {"<br>".join(self.inputs)}
                        <br><input type='submit' value='Submit {self.id}'>
                    </form>
                </fieldset>
               """