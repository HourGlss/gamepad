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

print("MASTER v0.3")
gamepad_active = False
try:
    gp = Gamepad(usb_hid.devices)
    gamepad_active = True
except:
    pass
gamepad_buttons = tuple([e for e in range(1, 20)])
pico_comm = busio.UART(
    tx=board.GP0,
    rx=board.GP1,
    baudrate=115200,
    timeout=.0001)
button_info = [
    ("sel", board.GP18, board.GP19),
    ("start", board.GP17, board.GP16),
    ("u", board.GP13, board.GP12),
    ("l", board.GP10, board.GP11),
    ("r", board.GP9, board.GP8),
    ("d", board.GP7, board.GP6),
    ("l1", board.GP5, board.GP4),
    ("l2", board.GP3, board.GP2)]
ljs = Joystick(board.GP27, board.GP26, board.GP22)
buttons = [Button(e[0], e[1], e[2]) for e in button_info]
print("SETUP COMPLETE")
read_size = 10
adjust_size = 0
fixing_data_len = False
while True:
    data = pico_comm.read(read_size - adjust_size)
    if data is not None:
        data_len = len(data)
        print(f"length of data: {data_len}")

        if data_len != 10:
            fixing_data_len = True
            adjust_size = 10 - data_len
            continue
        if fixing_data_len:
            fixing_data_len = False
            adjust_size = 0
        lbuttons = [e.value() for e in buttons]
        print(f"Buttons from Master {lbuttons}")
        rx, ry, *rbuttons = struct.unpack('bbbbbbbbbb', data)
        print(f"Buttons from Slave {rbuttons}")
        lx, ly, ls = ljs.values()
        print(f"{lx} {ly}   {rx} {ry}")
        all_buttons = rbuttons + lbuttons
        print(all_buttons)
        if gamepad_active:
            for i, button in enumerate(all_buttons):
                gamepad_button_num = gamepad_buttons[i]
                if button:
                    gp.release_buttons(gamepad_button_num)
                else:
                    gp.press_buttons(gamepad_button_num)
            gp.move_joysticks(x=rx, y=ry, z=lx, r_z=ly)
