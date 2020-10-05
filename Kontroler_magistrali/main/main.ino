#include <OneWire.h>

const byte ONEWIRE_PIN = 5;
OneWire onewire(ONEWIRE_PIN);
const char MESSAGE_LENGTH = 16;
char incomingMessage[MESSAGE_LENGTH];
char outgoingMessage[MESSAGE_LENGTH];

void setup() 
{
  // put your setup code here, to run once:
  while (!Serial);
  Serial.begin(115200);
  Serial.setTimeout(1000);
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
            Serial.write(byte(0x01));
          }
          else 
          {
            Serial.write(byte(0xFF));
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
            Serial.write(byte(0xFF));
      }
      break;

      // WRITE N BYTES
      case 'E': 
      {
        //Serial.print(strlen(incomingMessage)); // DEBUG PURPOSES
        if (strlen(incomingMessage) == 2)
        {
          if (incomingMessage[1] < 14) 
          {
            onewire.write_bytes((const uint8_t*)incomingMessage+2, incomingMessage[1], false);
          }
          else 
            Serial.write(byte(0xFF));
        }
        else 
          Serial.write(byte(0xFF));
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
            Serial.write(byte(0x01));
          }
          else
            Serial.write(byte(0xFF));
        }
        else
          Serial.write(byte(0xFF));
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
            onewire.select(rom);
            Serial.write(byte(0x01));

          }
          else
            Serial.write(byte(0xFF));
      }
      break;

      // DO A ROM SKIP
      case 'I': 
      {
          onewire.skip();
          Serial.write(byte(0x01));
      }
      break;

      // DEPOWER
      case 'J': 
      {
          onewire.depower();
          Serial.write(byte(0x01));
      }
      break;

      // RESET SEARCH TO BEGGINING
      case 'K': 
      {
          onewire.reset_search();
          Serial.write(byte(0x01));
      }
      break;

      // PERFORM A 1-WIRE SEARCH
      case 'L': 
      {
          if (strlen(incomingMessage) == 9) 
          {
            char addr[8];
              for (int i = 0; i < strlen(addr); i++) addr[i] = '\0';
            strncpy(addr, incomingMessage+1, 8);
            onewire.search(addr, true);
            Serial.write(byte(0x01));

          }
          else
            Serial.write(byte(0xFF));
      }
      break;

      /* // the rest are CRC checks
      case 'M': {

        }
      break;

      case 'N': {

        }
      break;

      case 'O': {

        }
      break;
      */
    }
      clear_message(incomingMessage);
  }
}

void clear_message(char* message) 
{
  for(int i = 0; i < MESSAGE_LENGTH; i++) message[i] = '\0';
}
