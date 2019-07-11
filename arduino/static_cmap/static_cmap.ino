#include <Adafruit_NeoPXL8.h>
#include "Colormap.h"

#define NUM_LED 240

int8_t pins[8] = { A3, A4, SDA, 5, 13, MISO, PIN_SERIAL1_TX, PIN_SERIAL1_RX };
Adafruit_NeoPXL8 leds(NUM_LED, pins, NEO_GRB);


void setup() {
  leds.begin();
  leds.setBrightness(255);
  for (int i=0; i<CALC_PIXELS; i++) {
    leds.setPixelColor(i, cmap[i][0], cmap[i][1], cmap[i][2]);
  }
  leds.show();
}

void loop() {
  // put your main code here, to run repeatedly:

}
