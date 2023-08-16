import board
import time
import busio
import struct
from fyx_joystick import Joystick
from fyx_button import Button
print("SLAVE")
pico_comm = busio.UART(
    tx=board.GP0,
    rx=board.GP1,
    baudrate=115200,
    timeout=.001)

b1 = Button("c", board.GP17, board.GP16)
b2 = Button("t", board.GP14, board.GP15)
b3 = Button("x", board.GP13, board.GP12)
b4 = Button("y", board.GP10, board.GP11)
b5 = Button("b", board.GP9, board.GP8)
b6 = Button("a", board.GP7, board.GP6)
b7 = Button("r1", board.GP5, board.GP4)
b8 = Button("r2", board.GP3, board.GP2)
time_last_sent = -1
js = Joystick(board.GP27, board.GP26, board.GP22)
print("SETUP COMPLETE")
while True:
    now = int(time.monotonic() * 100)
    if time_last_sent == -1 or now - time_last_sent > 20:
        x, y, s = js.values()
        var = struct.pack('bbbbbbbbbb', x, y, b1.value, b2.value, b3.value, b4.value, b5.value, b6.value, b7.value, b8.value)
        pico_comm.write(var)
