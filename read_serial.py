import serial

arduino_port = '/dev/ttyACM0'
baud_rate = 9600

# x is between 0 and 800, y is between 0 and 480
def readserial(comport, baudrate):

    ser = serial.Serial(comport, baudrate, timeout=0.1)         # 1/timeout is the frequency at which the port is read

    while True:
        # data is of form x<integer>y<integer> parse it with regex or smn
        data = ser.readline().decode().strip()
        if data:
            print(data)

if __name__ == '__main__':

    readserial(arduino_port, baud_rate)
