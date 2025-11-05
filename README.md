# touchscreen-macropad
## Getting this thing working
### Pinouts
sck  : 13

miso : 12

mosi : 11

cs   : 10

rst  : 9

int  : 7

### Setup Aruino
install arduino ide https://www.arduino.cc/en/software/

install these in arduino ide with dependencies
```
Adafruit RA8875 v 1.4.4
```
restart ide

plug arduino into computer

Select the board in board selector

in terminal, confirm port you're using with 
```
ls /dev/ttyACM0
```
then set read write perms
```
sudo chmod a+rw /dev/ttyACM0
```
press little arrow in top left of ide to send program to arduino

### If you want to play around with python - here's the starting point
```
pip install pyserial
```
change serial port in read_serial.py if needed