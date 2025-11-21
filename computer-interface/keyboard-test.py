from evdev import UInput, ecodes as e
import time

ui = UInput()

key_sequences = [
    [e.KEY_LEFTCTRL, e.KEY_LEFTSHIFT, e.KEY_P]
]
def sendKeyboard(i):
    time.sleep(2)

    for k in key_sequences[i]:
        ui.write(e.EV_KEY, k, 1)
    ui.syn()

    for k in key_sequences[i]:
        ui.write(e.EV_KEY, k, 0)
    ui.syn()

if __name__ == '__main__':
    sendKeyboard(0)
    ui.close()