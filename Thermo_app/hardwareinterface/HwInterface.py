import serial
from serial.tools import list_ports

class HwInterface:
    """ An interface for arduino-based hardware platform including DS18B20
    temperature sensor and an optional buzzer """

    # default arduino serial config is:
    # 8N1 (8 data bits, no parity, 1 stop bit)
    baud = 115200
    dataBits = serial.EIGHTBITS
    parity = serial.PARITY_NONE
    stopBits = serial.STOPBITS_ONE

    def __init__(self, port=None):
        self.port = port
        self.ser = serial.Serial()

    def __del__(self):
        if self.ser.is_open == True:
            self.ser.close()
        del self.ser
        del self.port
        print("DEBUG: Goodbye World!")


    def openComm(self):
        """ Opens specified USBVCP and check whether a recognizable device is
        presenting itself on that port """
        # check whether a communication channel already exist
        if self.ser.is_open == False:
            # check whether port specified is a valid port, if it is, open it
            list = list_ports.comports()
            if list == []:
                print("ERR: There are no serial ports available in your system resources!")
            else:
                for obj in list:
                    if self.port in obj.device:
                        print("DEBUG: Initializing communication port...")
                        self.ser.port = self.port
                        self.ser.baudrate = HwInterface.baud
                        self.ser.bytesize = HwInterface.dataBits
                        self.ser.parity = HwInterface.parity
                        self.ser.stopbits = HwInterface.stopBits
                        self.ser.open()
                        print("DEBUG: Done!")
                    else:
                        print("ERR: Sepcified port name not found in system resources!")
        else:
            print("ERR: Serial communication already opened on:", self.port)
        # TODO: try except clause!
        # TODO: present device type to the software interface!

    def closeComm(self):
        """ Closes specified USBVCP if open """
        if self.ser.is_open == True:
            print("DEBUG: Closing communication port...")
            self.ser.close()
            print("DEBUG: Done!")
        else:
            print("ERR: There is no open communication port!")

    def measTemp(self):
        """ Requests for temperature measurement """
        # TODO
        # get measTemp code from commands dictionary
        # send this code
        # check whether return message is OK
        # catch exceptions realed to comm port being not available
        pass

    def getTemp(self):
        """ Requests for available temperature measurement data """
        # TODO
        # catch exceptions realed to comm port being not available
        # get getTemp code from commands dictionary
        # ceck whether
        pass

    def measAndGetTemp():
        """ Combines measTemp() and getTemp() into one method """
        # TODO
        # catch exceptions realed to comm port being not available
        pass

    def activateBuzzer():
        """ OPTIONAL: Activates buzzer for unspecified amount of time """
        # optional TODO
        # catch exceptions realed to comm port being not available
        pass

    def deactivateBuzzer():
        """ OPTIONAL: Deactivates active buzzer """
        # optional TODO
        # catch exceptions realed to comm port being not available
        pass
