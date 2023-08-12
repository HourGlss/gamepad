import analogio
import digitalio


class Joystick:
    x_axis_pin: analogio.AnalogIn
    y_axis_pin: analogio.AnalogIn
    sel: digitalio.DigitalInOut
    min_dead: int  # Percentage values
    max_dead: int  # Percentage values

    def __init__(self, xpin, ypin, sel):
        self.x_axis_pin = analogio.AnalogIn(xpin)
        self.y_axis_pin = analogio.AnalogIn(ypin)
        self.sel = digitalio.DigitalInOut(sel)
        self.sel.switch_to_input(pull=digitalio.Pull.UP)
        self.min_dead = -3
        self.max_dead = 3

    def set_deadzone(self, min_dead, max_dead):
        self.min_dead = min_dead
        self.max_dead = max_dead

    def values(self):
        x = self.normalize(int(self.x_axis_pin.value))
        y = self.normalize(int(self.y_axis_pin.value))
        if self.min_dead <= x <= self.max_dead:
            x = 0
        if self.min_dead <= y <= self.max_dead:
            y = 0
        sel_value = not self.sel.value
        return x, y, sel_value

    def normalize(self, value):
        bounds = {
            "desired": {
                "lower": -127,
                "upper": 127
            },
            "actual": {
                "lower": 0,
                "upper": 65535
            }
        }

        return int(
            bounds['desired']['lower'] + (value - bounds['actual']['lower']) * (
                    bounds['desired']['upper'] - bounds['desired']['lower']) / (
                    bounds['actual']['upper'] - bounds['actual']['lower']))
