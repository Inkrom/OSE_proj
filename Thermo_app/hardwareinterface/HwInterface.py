import serial
from serial.tools import list_ports
from .commands import oneWireCommands, ds18b20Commands

class HwInterface:
    """ An interface for arduino-based hardware platform including DS18B20
    temperature sensor and an optional buzzer """

    # default arduino serial config is:
    # 8N1 (8 data bits, no parity, 1 stop bit)
    baud = 115200
    dataBits = serial.EIGHTBITS
    parity = serial.PARITY_NONE
    stopBits = serial.STOPBITS_ONE
    timeout = 0.5

    term_char = '58' # termination character as hex string

    def __init__(self, port=None):
        self.port = port
        self.ser = serial.Serial(timeout=HwInterface.timeout)

    def __del__(self):
        if self.ser.is_open == True:
            self.ser.close()
        del self.ser
        del self.port

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
                        #print("DEBUG: Initializing communication port...")
                        self.ser.port = self.port
                        self.ser.baudrate = HwInterface.baud
                        self.ser.bytesize = HwInterface.dataBits
                        self.ser.parity = HwInterface.parity
                        self.ser.stopbits = HwInterface.stopBits
                        self.ser.open()
                        #print("DEBUG: Done!")
                    else:
                        print("ERR: Sepcified port name not found in system resources!")
        else:
            print("ERR: Serial communication already opened on:", self.port)
        # TODO: try except clause!
        # TODO: present device type to the software interface!

    def closeComm(self):
        """ Closes specified USBVCP if open """
        if self.ser.is_open == True:
            #print("DEBUG: Closing communication port...")
            self.ser.close()
            #print("DEBUG: Done!")
        else:
            print("ERR: There is no open communication port!")

    def realizeTransaction(self, message):
        """ Does one data excahnge between PC and hardware with remination
        character defined in class-wide attribute. Takes message to be sent,
        returns response from hardware """
        self.ser.write(bytes.fromhex(message))
        #print(message)
        response = self.ser.read_until(bytes.fromhex(HwInterface.term_char))
        #print(response)
        return response

    def initializeBus(self):
        """ Initializes every 1-Wire Bus transaction as specified in the
        interface documentation """
        # 1st: reset the bus
        message = oneWireCommands['reset'] + HwInterface.term_char
        #print("Trying to reset 1-Wire Bus with message: ", message)
        response = self.realizeTransaction(message)

        # 2nd: skip ROM because on the bus is only one 1-Wire sensor
        message = oneWireCommands['skip_rom'] + HwInterface.term_char
        response = self.realizeTransaction(message)

    def measTemp(self):
        """ Requests for temperature measurement """
        # TODO
        #initialize bus
        self.initializeBus()
        # message sensor to convert temperature
        message = oneWireCommands['write_byte'] + ds18b20Commands['convert_temp'] + HwInterface.term_char
        response = self.realizeTransaction(message)

        # TODO: error catching

    def getTemp(self):
        """ Requests for available temperature measurement data """
        # TODO
        #initialize bus
        self.initializeBus()
        # message sensor to prepare scratchpad to be read
        message = oneWireCommands['write_byte'] + ds18b20Commands['read_scratch'] + HwInterface.term_char
        response = self.realizeTransaction(message)
        # read 9 bytes of scratchpad from sensor
        nOfBytes = '09'
        message = oneWireCommands['read_bytes'] + nOfBytes + HwInterface.term_char
        self.ser.write(bytes.fromhex(message))
        response = self.ser.read(int(nOfBytes))
        # TODO: check wheter CRC8 is valid
        crc8 = response[-1]
        # decode temperature value to Celsius
        # 1st: evaluate sign
        temp_encoded = response[:2]
        sign_mask = b'\xF8' # 0b11111000
        if (response[1] & sign_mask[0]) == 0:
            temp_sign = 1
        else:
            temp_sign = -1
        # mask sign bits
        sign_mask = b'\x07' # 0b00000111
        temp_H = (response[1] & sign_mask[0])*16
        temp_L = response[0] >> 4
        decim_mask = b'\x0F' # 0b00001111
        temp_flt = (response[0] & decim_mask[0])*(2**(-4))

        temp = (temp_H + temp_L + temp_flt)*temp_sign
        return temp

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
