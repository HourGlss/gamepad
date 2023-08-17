import board
import time
import busio
import struct
from fyx_joystick import Joystick
from fyx_button import Button

print("SLAVE v1.1")
time.sleep(.5)
pico_comm = busio.UART(
    tx=board.GP0,
    rx=board.GP1,
    baudrate=115200)
button_info = [
    ("c", board.GP17, board.GP16),
    ("t", board.GP14, board.GP15),
    ("x", board.GP13, board.GP12),
    ("y", board.GP10, board.GP11),
    ("b", board.GP9, board.GP8),
    ("a", board.GP7, board.GP6),
    ("r1", board.GP5, board.GP4),
    ("r2", board.GP3, board.GP2),
]
time_last_sent = -1
js = Joystick(board.GP27, board.GP26, board.GP22)
buttons = [Button(e[0], e[1], e[2]) for e in button_info]
print("SETUP COMPLETE")

while True:
    now = int(time.monotonic() * 100)
    if time_last_sent == -1 or now - time_last_sent > 20:
        x, y, s = js.values()
        rbuttons = [e.value() for e in buttons]
        var = struct.pack('bbbbbbbbbb', x, y, rbuttons[0], rbuttons[1], rbuttons[2], rbuttons[3], rbuttons[4],
                          rbuttons[5], rbuttons[6], rbuttons[7])
        pico_comm.write(var)
