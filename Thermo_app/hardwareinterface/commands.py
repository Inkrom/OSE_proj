""" Contains hex strings dictionary for different 1-Wire Bus operations and
DS18B20 temperature sensor commands """

oneWireCommands = {
'reset' : '41',
'skip_rom' : '49',
'write_byte' : '44',
'write_bytes' : '45',
'read_byte' : '46',
'read_bytes' : '47',
# that's not all, but several omitted due to lack of use in this implementation
}

ds18b20Commands = {
'convert_temp' : '44',
'read_scratch' : 'BE',
# that's also not all of available commands, cound use writing to sratchpad to
# set sensor's parameters in the future
}
