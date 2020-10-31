import sys
sys.path.append("..")
from hardwareinterface.HwInterface import HwInterface

hardWareInt = HwInterface() # sets calss-wide attribute 'port' to 'None'

hardWareInt.port = '/dev/ttyUSB0' # sets class-wide 'port' attr. outside of the constructor

hardWareInt.openComm() # opens communication port
hardWareInt.openComm() # tries to open the same instance the second time

hardWareInt.closeComm() # closes previosuly opened communication port
hardWareInt.closeComm() # tries the same again
