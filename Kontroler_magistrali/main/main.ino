#include <OneWire.h>

const byte ONEWIRE_PIN = 5;
OneWire onewire(ONEWIRE_PIN);
const char MESSAGE_LENGTH = 16;
char incomingMessage[MESSAGE_LENGTH];
char outgoingMessage[MESSAGE_LENGTH];
const byte ERROR_BYTE = byte(0xFF);
const byte SUCCESS_BYTE = byte(0x01);

void setup() 
{
  // put your setup code here, to run once:
  while (!Serial);
  Serial.begin(115200);
  Serial.setTimeout(250);
}

void loop() 
{
  // put your main code here, to run repeatedly:
  handleSerial();
}

void handleSerial() 
{
  if (Serial.available() > 0) 
  {
      Serial.readBytesUntil('X', incomingMessage, 16);
      
    switch (incomingMessage[0]) 
    {

      // RESET
      case 'A': 
      {
          uint8_t response = onewire.reset();
          Serial.write(response);
      }
      break;

      // WRITE A BIT
      case 'B': 
      {
          if (incomingMessage[1] != '\0') 
          {
            onewire.write_bit(uint8_t(incomingMessage[1]));
            Serial.write(SUCCESS_BYTE);
          }
          else 
          {
            Serial.write(ERROR_BYTE);
          }
      }
      break;

      // READ A BIT
      case 'C': 
      {
          byte data;
          data = onewire.read_bit();
          Serial.write(data);
      }
      break;

      // WRITE A BYTE
      case 'D': 
      {
          if (incomingMessage[1] != '\0') 
          {
            onewire.write(uint8_t(incomingMessage[1]), 0);
            Serial.write(incomingMessage[1]);
          }
          else 
            Serial.write());
      }
      break;

      // WRITE N BYTES
      case 'E': 
      {
        //Serial.print(strlen(incomingMessage)); // DEBUG PURPOSES
        if (strlen(incomingMessage) == 2)
        {
          if (incomingMessage[1] <= 14) 
          {
            onewire.write_bytes((const uint8_t*)incomingMessage+2, incomingMessage[1], false);
          }
          else 
            Serial.write(ERROR_BYTE);
        }
        else 
          Serial.write(ERROR_BYTE);
      }
      break;

      // READ A BYTE
      case 'F': 
      {
          byte data = onewire.read();
          Serial.write(data);
      }
      break;

      // READ N BYTES
      case 'G': 
      {
        clear_message(outgoingMessage);
        if (strlen(incomingMessage) == 2)
        {
          if (incomingMessage[1] <= 16)
          {
            onewire.read_bytes(outgoingMessage, uint16_t(incomingMessage[1]));
            Serial.write(outgoingMessage, incomingMessage[1]);
            Serial.write(SUCCESS_BYTE);
          }
          else
            Serial.write(ERROR_BYTE);
        }
        else
          Serial.write(ERROR_BYTE);
      }
      break;

      // DO A ROM SELECT
      case 'H': 
      {
          if (strlen(incomingMessage) == 9) 
          {
            char rom[8];
              for (int i = 0; i < strlen(rom); i++) rom[i] = '\0';
            strncpy(rom, incomingMessage+1, 8);
            Serial.write(SUCCESS_BYTE);
            onewire.select(rom);
          }
          else
            Serial.write(ERROR_BYTE);
      }
      break;

      // DO A ROM SKIP
      case 'I': 
      {
          onewire.skip();
          Serial.write(SUCCESS_BYTE);
      break;

      // DEPOWER
      case 'J': 
      {
          onewire.depower();
          Serial.write(SUCCESS_BYTE);
      }
      break;

      // RESET SEARCH TO BEGGINING
      case 'K': 
      {
          onewire.reset_search();
          Serial.write(SUCCESS_BYTE);
      }
      break;

      // PERFORM A 1-WIRE SEARCH
      case 'L': 
      {
          char addr[8];
            for (int i = 0; i < strlen(addr); i++) addr[i] = '\0';
          if (onewire.search(addr, true))
          {
            Serial.write(SUCCESS_BYTE);
            Serial.write(addr, 8);
          }
          else
            Serial.write(ERROR_BYTE);
      }
      break;

      // COMPUTE DS 8 bit CRC
      case 'M': 
      {
        char crc = 0;
        if (strlen(incomingMessage) > 2)
        {
          if (incomingMessage[1] <= 14)
          {
            crc = onewire.crc8(incomingMessage+2, incomingMessage[1]);
            Serial.write(byte(crc));
          }
          else
            Serial.write(ERROR_BYTE);
        }
        else
          Serial.write(ERROR_BYTE);
      }
      break;

      /* // COMPUTE DS 16 bit CRC
      case 'N': 
      {
        uint16_t crc;
        if (strlen(incomingMessage) > 2)
        {
          if (incomingMessage[1] <= 14)
          {
            crc = onewire.crc16(incomingMessage+2, incomingMessage[1]);
            Serial.write(crc);
          }
          else
            Serial.write(byte(0xFF));
        }
        else
          Serial.write(byte(0xFF));
      }
      break; */

      default:
        Serial.write(ERROR_BYTE);
      break;
    }
      clear_message(incomingMessage);
  }
}

void clear_message(char* message) 
{
  for(int i = 0; i < MESSAGE_LENGTH; i++) message[i] = '\0';
}
