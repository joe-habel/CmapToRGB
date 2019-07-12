#include <string.h>
#include <Arduino.h>
#include <SPI.h>
#if not defined (_VARIANT_ARDUINO_DUE_X_) && not defined (_VARIANT_ARDUINO_ZERO_)
  #include <SoftwareSerial.h>
#endif

#include <Adafruit_BLE.h>
#include <Adafruit_BluefruitLE_SPI.h>
#include <Adafruit_BluefruitLE_UART.h>

#define PACKET_CMAP_LEN                 (19)

//    READ_BUFSIZE            Size of the read buffer for incoming packets
#define READ_BUFSIZE                    (19)


/* Buffer to hold incoming characters */
uint8_t packetbuffer[READ_BUFSIZE+1];

/**************************************************************************/
/*!
    @brief  Waits for incoming data and parses it
*/
/**************************************************************************/
uint8_t readPacket(Adafruit_BLE *ble, uint16_t timeout) 
{
  uint16_t origtimeout = timeout, replyidx = 0;

  memset(packetbuffer, 0, READ_BUFSIZE);

  while (timeout--) {
    if (replyidx >= 20) break;
    if (replyidx == PACKET_CMAP_LEN) break;

    while (ble->available()) {
      char c =  ble->read();
      Serial.print(c);
      if (c == '!') {
        replyidx = 0;
      }
      packetbuffer[replyidx] = c;
      replyidx++;
      timeout = origtimeout;
    }
    
    if (timeout == 0) break;
    delay(1);
  }

  packetbuffer[replyidx] = 0;  // null term
  if (!replyidx)  // no data or timeout 
    return 0;
  if (packetbuffer[0] != '!')  // doesn't start with '!' packet beginning
    return 0;
  
  // check checksum!
  int16_t xsum = 0;
  int16_t checksum = packetbuffer[replyidx-2] << 8 | packetbuffer[replyidx-1];

  for (uint8_t i=0; i<replyidx-2; i++) {
    xsum += packetbuffer[i];
  }
  xsum = ~xsum;

  // Throw an error message if the checksum's don't match
  if (xsum != checksum)
  {
    return 0;
  }
  
  // checksum passed!
  return replyidx;
}
