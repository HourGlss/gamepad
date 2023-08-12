import board
import digitalio


class Button:
    line_out: digitalio.DigitalInOut
    line_in: digitalio.DigitalInOut
    name: str

    def __init__(self, name, line_in, line_out):
        self.name = name
        self.line_in = digitalio.DigitalInOut(line_in)
        self.line_out = digitalio.DigitalInOut(line_out)
        self.line_in.switch_to_input(pull=digitalio.Pull.DOWN)
        self.line_out.switch_to_input(pull=digitalio.Pull.UP)

    def value(self):
        return self.line_in.value
