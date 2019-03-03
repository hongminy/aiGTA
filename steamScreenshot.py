from pynput.keyboard import Key, Controller
from time import sleep
keyboard = Controller()

while True:
    # Press and release f12
    keyboard.press(Key.f12)
    keyboard.release(Key.f12)
    sleep(2)
