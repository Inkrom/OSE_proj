import sys, time
sys.path.append("..")
from hardwareinterface.HwInterface import HwInterface

hardWareInt = HwInterface() # passing no args sets calss-wide attribute 'port' to 'None'

hardWareInt.port = 'COM6' # sets class-wide 'port' attr. outside of the constructor

hardWareInt.openComm() # opens communication port
#hardWareInt.openComm() # tries to open the same instance the second time
try:
    print("Hello World!")
    while True:
        hardWareInt.measTemp()
        time.sleep(1) # TODO: calculate converison time
        temp = hardWareInt.getTemp()
        print("Temperature: ", temp)
except KeyboardInterrupt: # press Ctrl-Z or Ctrl-C to stop the program
    print("Goodbye World!")
    pass

hardWareInt.closeComm() # closes previosuly opened communication port
#hardWareInt.closeComm() # tries the same again
