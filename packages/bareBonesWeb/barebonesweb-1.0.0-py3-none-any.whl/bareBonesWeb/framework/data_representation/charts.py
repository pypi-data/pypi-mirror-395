from itertools import cycle, islice
from typing import overload

class color:
    r: int
    g: int
    b: int

    @overload
    def __init__(self, r: int, g: int, b: int) -> None:
        self.color = (r, g, b)
    @overload
    def __init__(self, hex: str) -> None: 
        pass

    def __init__(self, r: Union[int, str], g: Optional[int] = None, b: Optional[int] = None) -> None: #type: ignore
        if isinstance(r, str):
            hex_str = r.strip("#")
            if len(hex_str) != 6:
                raise ValueError("Hex string must be 6 characters long (e.g. #RRGGBB)")
            self.r = int(hex_str[0:2], 16)
            self.g = int(hex_str[2:4], 16)
            self.b = int(hex_str[4:6], 16)
        elif g is not None and b is not None:
            self.r = r
            self.g = g
            self.b = b
        else:
            raise TypeError("Color must be initialized with (r, g, b) integers or a (hex) string.")
        
    def __str__(self) -> str:
        return f"rgb({self.r} {self.g} {self.b})"
    
class coordinates:
    values: list[tuple[int, int]]

    def __init__(self, data_name: str, values: list[tuple[int, int]]) -> None:
        """
        :param data_name: Name of the data
        :type data_name: str
        :param values: Co-ordinate Values
        :type values: list[tuple[int, int]]
        """
        self.data_name = data_name
        self.values = values

class data:
    values: list[int | tuple[int, str]]

    def __init__(self, data_name: str, values: list[int | tuple[int, str]]) -> None:
        self.data_name = data_name
        self.values = values

    def add_value(self, value: int | tuple[int, str]):
        self.values.append(value)

def piechart(data, accents = [color(128, 0, 0), color(0, 128, 0), color(0, 0, 128)], diameter="200px"):
    # 1. Prepare Colors
    accent_cycle = cycle(accents)
    accents_for_data = list(islice(accent_cycle, len(data.values)))

    # 2. Calculate Total Sum
    values = []
    for item in data.values:
        # Extracts the value, handling both integer/float and (value, label) tuple formats
        value = item if isinstance(item, (int, float)) else item[0]
        values.append(value)
        
    sum_of_vals = sum(values)

    # If the sum is zero, return an empty chart to prevent division by zero
    if sum_of_vals == 0:
        return f"""
            <fieldset style='width: {diameter}; padding: 7px;'>
                <legend>{data.data_name}</legend>
                <div style='width: calc({diameter} - 14px); height: calc({diameter} - 14px); border-radius: 50%; background-color: #ccc;'><br></div>
            </fieldset>
            """

    deg_per_unit = 360 / sum_of_vals

    grad = []
    current_angle = 0
    
    for index, value in enumerate(values):
        color = accents_for_data[index]
        
        segment_degrees = value * deg_per_unit
        
        next_angle = current_angle + segment_degrees
        
        grad.append(f"{color} {current_angle:.2f}deg {next_angle:.2f}deg")
        
        current_angle = next_angle

    return f"""
        <fieldset style='width: {diameter}; padding: 7px;'>
            <legend><h3>{data.data_name}</h3></legend>

            <div style='width: calc({diameter} - 7px); height: calc({diameter} - 7px); border-radius: 50%; background-image: conic-gradient({", ".join(grad)});'></div>
        </fieldset>
        """