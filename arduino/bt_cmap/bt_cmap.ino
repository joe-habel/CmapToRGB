#include <Arduino.h>
#include <SPI.h>
#include <Adafruit_BLE.h>
#include <Adafruit_BluefruitLE_SPI.h>
#include <Adafruit_BluefruitLE_UART.h>
#include <Adafruit_NeoPXL8.h>

#include "BluefruitConfig.h"
#include "Colormap.h"

#define NUM_LED 240 //per strip
#define NUM_STRIP 2 //number of strips used

#define FACTORYRESET_ENABLE         1
#define MINIMUM_FIRMWARE_VERSION    "0.6.6"
#define MODE_LED_BEHAVIOUR          "MODE"

int8_t pins[8] = { A3, A4, SDA, 5, 13, MISO, PIN_SERIAL1_TX, PIN_SERIAL1_RX };
Adafruit_NeoPXL8 leds(NUM_LED, pins, NEO_GRB);

Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

uint8_t readPacket(Adafruit_BLE *ble, uint16_t timeout);
extern uint8_t packetbuffer[];


void setup() {
  pinMode(13, OUTPUT);
  leds.begin();
  leds.setBrightness(255);
  ble.echo(false);
  if (NUM_LED*NUM_STRIP == CALC_PIXELS) {
    for (int i=0; i<CALC_PIXELS; i++) {
      leds.setPixelColor(i, cmap[i][0], cmap[i][1], cmap[i][2]);
    }
  }
  else {
    uint16_t px_count = NUM_LED*NUM_STRIP;
    for (int i=0; i<px_count; i++) {
      leds.setPixelColor(i, 0, 0, 0);
    }
  }
  leds.show();
}

void loop() {
  while (! ble.isConnected()) {
      for (int i=0; i<5; i++){
          digitalWrite(13, HIGH);
          delay(50);
          digitalWrite(13, LOW);
      }
      delay(250);
  }
  uint8_t len = readPacket(&ble, BLE_READPACKET_TIMEOUT);
  if (len != 0) {
    uint16_t start_led = packetbuffer[1] << 8 | packetbuffer[2];
    uint16_t end_led = packetbuffer[3] << 8 | packetbuffer[4];
    uint8_t offset = 5;
    for (int i=start_led; i < end_led; i++){
      uint8_t red = packetbuffer[offset];
      offset ++;
      uint8_t green = packetbuffer[offset];
      offset ++;
      uint8_t blue = packetbuffer[offset];
      offset ++;
      leds.setPixelColor(i, red, green, blue);
    }
    leds.show();
  }
  ble.print(len);

}
