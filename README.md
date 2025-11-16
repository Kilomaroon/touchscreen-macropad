
# Setup
## Hardware Pinouts
| RA8875 Pin  | Arduino Uno Pin
| ----- | --------------------------------------------------- |
|SCK|13|
|MISO|14|
|MOSI|11|
|CS|10|
|RST|9|
|INT|7|

## Arduino 
Install [Arduino IDE](https://www.arduino.cc/en/software/)
- Within the IDE, install the `Adafruit RA8875 v 1.4.4` library and dependencies.
- Restart the IDE.
- Connect the Arduiono to your PC and select it in the Arduino IDE's board selector.
- Press the little arrow in top left of IDE window to program the Arduino Uno.

### If you have trouble programming the Arduino
In terminal, you can confirm the port with: 
```
ls /dev/ttyACM0
```
and set read write perms with:
```
sudo chmod a+rw /dev/ttyACM0
```


## Python
Install the pyserial library with `pip install pyserial`.

Section to be updated

# Commit Message Terminology
| Word  | Definition
| ----- | --------------------------------------------------- |
| **Evert** | *Verb, transitive.* To turn inside out or outwards. From Late Latin *ēvertere* (“to turn (an item of clothing) inside out”), Latin *ēvertere*, present active infinitive of *ēvertō* (“to turn upside down; to overturn; to reverse”), from *ē-* (variant of *ex-* (prefix meaning ‘out, away’)) + *vertō* (“to reverse; to revolve, turn; to turn around”) (ultimately from Proto-Indo-European **wert-* (“to rotate, turn”)) [1]. |

### References
[1] Wiktionary contributors, “evert,” Wiktionary. Accessed: Nov. 11, 2025. [Online]. Available: https://en.wiktionary.org/w/index.php?title=evert&oldid=85391271
