# Happy Birthday!
We made you a little thing! Hope you enjoy it! We've been working on this for a bit and think you'll have a lot of fun tinkering with it!

To clarify: this is a touchscreen macropad we've made for you. It connects a little touchscreen display to an arduino - which sends your inputs over serial. You shouldn't need to mess with this side much though (unless you want to tweak the visuals) as the actual macro assignment is on the python end in the `computer-interface` folder.

# Setup
## Hardware Pinouts
You shouldn't need to rewire this - but just in case...
| RA8875 Pin  | Arduino Uno Pin
| ----- | --------------------------------------------------- |
|SCK|13|
|MISO|12|
|MOSI|11|
|CS|10|
|RST|9|
|INT|7|
|VIN|Vin|
|GND|GND|

## Arduino 
Install [Arduino IDE](https://www.arduino.cc/en/software/)
- Within the IDE, install the `Adafruit RA8875 v 1.4.4` and `Adafruit GFX` libraries and dependencies.
- Restart the IDE.
- Connect the Arduino to your PC and select it in the Arduino IDE's board selector.
- Press the little arrow in top left of IDE window to program the Arduino Uno.
- (If you are running Wayland, you may have trouble running the IDE---the easiest workaround is to run it in XWayland (ensure you have XWayland installed first))

### Modifying Button Layout
The buttons are laid out on the touchscreen in a rectangular layout. The number of columns and rows in the layout, as well as the margin between the buttons, can be configured by editing the `BUTTON_COLS`, `BUTTON_ROWS`, and `BUTTON_MARGIN` macros in the `touchscreen-macropad.ino` file. The button labels can be configured by editing the string array `numerals` in the same file.

## Computer
On the computer side, this sets up a systemd service to monitor your computer's serial connection and receive commands from the Arduino, then trigger keypress events using `evdev`. 

It also sets up a few udev rules to automatically run/stop the service when the macropad is connected/disconnected, and to make a symlink so the service doesn't have to worry about which serial port the Arduino is connected to. (There's also an optional additional udev rule that will send a desktop notification when the macropad is plugged in, mostly because I sort of set that up by accident when trying to figure out how to do the systemd service.)

### Installation
Ensure you have the system packages `python3-evdev` ([documentation](https://python-evdev.readthedocs.io/en/latest/)) and `python3-serial` ([documentation](https://www.pyserial.org/docs)) installed.
* (they should already be installed on Mint [NO THEY ARE NOT] [INSTALL THEM])
* On Arch these can be found as [`python-evdev`](https://archlinux.org/packages/extra/x86_64/python-evdev/) and [`python-pyserial`](https://archlinux.org/packages/extra/any/python-pyserial/)
* After installation, you may need to reboot in order for the systemd service to run properly (you may see error messages about missing dependencies until you do this).

From the `computer-interface` directory, make the `setup.sh` file executable using
```bash
chmod +x setup.sh
```

Then run it (sudo required) using
```bash
sudo ./setup.sh
```

Make sure `/usr/local/bin/touch-macropad-service.py` is readable by your user, if it is not already.
```bash
sudo chmod 644 /usr/local/bin/touch-macropad-service.py
```

If you make any changes to the files after the initial installation, you may have to run 
```bash
sudo udevadm --reload
```
to reload your udev rules, or
```bash
sudo systemctl daemon-reload
```
to reload your systemd manager config in order for them to take effect.

### Configuring Functions
To configure the functions of each button, edit the `key_sequences` dict in `touch-macropad-service.py`. You can configure a keypress or combination of keypresses to be sent when each button is pressed (+) or released (-). The default setup is as follows:

| Button | Press  | Release   |
| ------ | -----  | --------- |
| 0      | CTRL-S | \<nothing\> |
| 1      | CTRL-C | \<nothing\> |
| 2      | CTRL-V | \<nothing\> |
| 3      | CTRL-C | CTRL-V    |

### Further Configuration
If you'd like to screw further with this side of things, much of it was informed by/adapted from the examples in the `PySerial` docs, available [here](https://www.pyserial.org/docs/linux-serial). The general structure is that `98-touch-macropad.rules` contains the udev rules, one of which establishes a dependency on `touch-macropad-service`, which is defined by the `touch-macropad-service.conf`, `touch-macropad-service.py`, and `touch-macropad-service.service` files. 

If you are making changes, you may find it useful to monitor the systemd logs for `touch-macropad-service` using
```bash
journalctl -f -u touch-macropad-service
```

### (Optional) Device Connection Notifications
If desired, the udev configuration can be modified to send a desktop notification when the device is connected. To do so, uncomment the last line in `computer-interface/98-touch-macropad.rules` and copy `computer-interface/arduino-connected.sh` to `/usr/local/bin/arduino-connected.sh` with:
```bash
sudo cp computer-interface/arduino-connected.sh /usr/local/bin/arduino-connected.sh
```

# Soundboard Functionality

Now also works as a soundboard with Pipewire.
See `touch-macropad-service/cfg.py` for examples of how to configure.

Sound files by default go in `/usr/local/bin/touch-macropad/sound/` (symlink it to your data directory of choice or edit it in the config).
If you see errors in `journalctl` about sound files not existing, make sure the path is not made inaccessible by directives in `touch-macropad-service.service`.

# Commit Message Glossary
| Word  | Definition
| ----- | --------------------------------------------------- |
| **Evert** | *Verb, transitive.* To turn inside out or outwards. From Late Latin *ēvertere* (“to turn (an item of clothing) inside out”), Latin *ēvertere*, present active infinitive of *ēvertō* (“to turn upside down; to overturn; to reverse”), from *ē-* (variant of *ex-* (prefix meaning ‘out, away’)) + *vertō* (“to reverse; to revolve, turn; to turn around”) (ultimately from Proto-Indo-European **wert-* (“to rotate, turn”)) [1]. |

### References
[1] Wiktionary contributors, “evert,” Wiktionary. Accessed: Nov. 11, 2025. [Online]. Available: https://en.wiktionary.org/w/index.php?title=evert&oldid=85391271
