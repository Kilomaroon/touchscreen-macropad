# touchscreen-macropad
## Getting this thing working
1. Setup Aruino
install arduino ide https://www.arduino.cc/en/software/
install these in arduino ide with dependencies
```
Adafruit RA8875 v 1.4.4
Streaming
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
press little arrow in top left of ide to send program to arduino (note to not have th epyhton code running when you do this bc it messes it up)

2. If you want to play around with python - here's the starting point
```
pip install pyserial
```
change serial port in read_serial.py if needed