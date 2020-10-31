import serial
from serial.tools import list_ports

port = 'dev/ttyUSB1'
list = list_ports.comports()
print(port)
for obj in list:
    if port in obj.device:
        print("True")
