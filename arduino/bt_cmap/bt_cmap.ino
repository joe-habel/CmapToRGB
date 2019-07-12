#include <Arduino.h>
#include <SPI.h>
#include <Adafruit_BLE.h>
#include <Adafruit_BluefruitLE_SPI.h>
//#include <Adafruit_BluefruitLE_UART.h>
#include <Adafruit_NeoPXL8.h>

#include "BluefruitConfig.h"
//#include "Colormap.h"

#if SOFTWARE_SERIAL_AVAILABLE
  #include <SoftwareSerial.h>
#endif

#define NUM_LED 240 //per strip
#define NUM_STRIP 2 //number of strips used

#define FACTORYRESET_ENABLE         1

int8_t pins[8] = { A3, A4, SDA, 5, 13, MISO, PIN_SERIAL1_TX, PIN_SERIAL1_RX };
Adafruit_NeoPXL8 leds(NUM_LED, pins, NEO_GRB);

Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

uint8_t readPacket(Adafruit_BLE *ble, uint16_t timeout);
extern uint8_t packetbuffer[];
bool connection;

void setup() {
  while (!Serial);  // required for Flora & Micro
  delay(500);

  leds.begin();
  leds.setBrightness(255);
  
  
  //if (NUM_LED*NUM_STRIP == CALC_PIXELS) {
  //  for (int i=0; i<CALC_PIXELS; i++) {
  //    leds.setPixelColor(i, cmap[i][0], cmap[i][1], cmap[i][2]);
  //  }
 // }
  //else {
    for (int i=0; i<NUM_LED*NUM_STRIP; i++) {
      leds.setPixelColor(i, 0, 0, 0);
    }
  leds.show();
  
  Serial.begin(115200);
  if ( !ble.begin(VERBOSE_MODE) )
  {
    Serial.println("Couldn't find Bluefruit, make sure it's in CoMmanD mode & check wiring?");
  }
  
  if ( FACTORYRESET_ENABLE )
  {
    /* Perform a factory reset to make sure everything is in a known state */
    Serial.println("Performing a factory reset: ");
    if ( ! ble.factoryReset() ){
      Serial.println("Couldn't factory reset");
    }
  }
  ble.echo(false);

  ble.verbose(false);
}

void loop() {
  if (!ble.isConnected()) {
    Serial.println("Waiting for connection");
    while (! ble.isConnected()) {
        delay(250);
        connection = ble.isConnected();
    }
    Serial.println("Connected!");
     ble.setMode(BLUEFRUIT_MODE_DATA);
  }
  
  uint8_t len = readPacket(&ble, BLE_READPACKET_TIMEOUT);
  if (len != 0) {
    uint16_t start_led = packetbuffer[1] << 8 | packetbuffer[2];
    uint16_t end_led = packetbuffer[3] << 8 | packetbuffer[4];
    Serial.print("Starting position: ");
    Serial.print(start_led);
    Serial.print(", Ending position: ");
    Serial.println(end_led);
    uint8_t offset = 5;
    for (int i=start_led; i < end_led; i++){
      uint8_t red = packetbuffer[offset];
      offset ++;
      uint8_t green = packetbuffer[offset];
      offset ++;
      uint8_t blue = packetbuffer[offset];
      offset ++;
      Serial.print("Pixel :");
      Serial.print(i);
      Serial.print(" R");
      Serial.print(red);
      Serial.print(" G");
      Serial.print(green);
      Serial.print(" B");
      Serial.println(blue);
      leds.setPixelColor(i, red, green, blue);
    }
    leds.show();
  }
 
  //ble.print(len);

}
