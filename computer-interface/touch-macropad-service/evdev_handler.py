from evdev import UInput, ecodes

class EvdevHandler():
    def __init__(self, logger=None):
        self.ui = UInput()
        self.logger = logger

    def handle(self, key_sequence):
        """Send a series of keys using evdev."""

        for k in key_sequence:
            self.ui.write(ecodes.EV_KEY, k, 1)
        self.ui.syn()

        for k in key_sequence:
            self.ui.write(ecodes.EV_KEY, k, 0)
        self.ui.syn()

    def close(self):
        self.ui.close()
