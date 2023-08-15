import board
import analogio
import time
import digitalio
import busio
import usb_hid
from hid_gamepad import Gamepad
import struct
from fyx_joystick import Joystick
from fyx_button import Button

print("MASTER")
gp = Gamepad(usb_hid.devices)
gamepad_buttons = tuple([e for e in range(1, 20)])
pico_comm = busio.UART(
    tx=board.GP0,
    rx=board.GP1,
    baudrate=115200,
    timeout=.001)
button_info = [
    ("sel", board.GP18, board.GP19),
    ("start", board.GP17, board.GP16),
    ("z", board.GP14, board.GP15),
    ("u", board.GP13, board.GP12),
    ("l", board.GP10, board.GP11),
    ("r", board.GP9, board.GP8),
    ("d", board.GP7, board.GP6),
    ("l1", board.GP5, board.GP4),
    ("l2", board.GP3, board.GP2)]
ljs = Joystick(board.GP27, board.GP26, board.GP22)
buttons = [Button(e[0], e[1], e[2]) for e in button_info]
print("SETUP COMPLETE")
while True:
    data = pico_comm.read(3)
    if data is not None:
        lbuttons = [e.value for e in buttons]
        rx, ry, rs, *rbuttons = struct.unpack('bbbbbbbbbbb', data)
        lx, ly, ls = ljs.values()
        all_buttons = [rs, ls] + rbuttons + lbuttons
        for i, button in enumerate(all_buttons):
            gamepad_button_num = gamepad_buttons[i]
            if button:
                gp.release_buttons(gamepad_button_num)
            else:
                gp.press_buttons(gamepad_button_num)
        gp.move_joysticks(x=rx, y=ry, z=lx, r_z=ly)