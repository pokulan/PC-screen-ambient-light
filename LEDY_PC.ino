#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif
#define PIN            3 		// PC HOUSING WS2812 LEDS PIN
#define NUMPIXELS      32		// PC HOUSING LEDS COUNT
#define PIN_LCD            5	// AMBIENT WS2811 LEDS PIN
#define NUMPIXELS_LCD      28	// AMBIENT WS2811 LEDS COUNT
short n = 11;
short R = 0;
short G = 0;
short B = 255;
short curR = R;
short curG = G;
short curB = B;
short tryb = 3;
short s = 50;
short power = 1;
float help = PI;

bool dir = 0;
short shift_led = n;
short shift_led2 = 1;

short meteor_led = 1;
short meteor_led2 = 0;

char buffer[90];
unsigned long t_time = millis();

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels_lcd = Adafruit_NeoPixel(NUMPIXELS_LCD, PIN_LCD, NEO_GRB + NEO_KHZ800);

int delayval = 100; // delay for half a second

void read_settings(){
  power = buffer[84];
  if(power == 0) pixels.setBrightness(0);
  else pixels.setBrightness(255);
  tryb = buffer[85];
  s = buffer[86];
  R = buffer[87];
  G = buffer[88];
  B = buffer[89];
}

void readSerial(){
  if (Serial.available() > 0) {
      Serial.readBytes(buffer, 90);
      
      for(int z = 0; z < 28; z++){
        pixels_lcd.setPixelColor(z, pixels.Color(buffer[z * 3], buffer[z * 3 + 1], buffer[z * 3 + 2]));
      }
      pixels_lcd.show();
      read_settings();

      ///////////////////////////////////// PC DECORATIONS RELOAD
      reload_pc_light();
      delay(10);
      reload_pc_light();
      
  }
}

void reload_pc_light(){
  if(tryb == 0 && power == 1){ ///////////////////////////////////// METEOR
    pixels.setBrightness(255);
    if(millis() - t_time > (220 - (s * 2))){
      t_time = millis();
      if(meteor_led < n){
        meteor_led ++;
      }else{
        if(meteor_led2 < n){
          meteor_led2 ++;
        }else{
          meteor_led = 1;
          meteor_led2 = 0;
        }
      }
    }
    for (int i = 0; i < meteor_led; i++) {
      pixels.setPixelColor(i, pixels.Color(R, G, B));
    }
    for (int i = 0; i < meteor_led2; i++) {
      pixels.setPixelColor(i, pixels.Color(0, 0, 0));
    }
  }////////////////////////////////////////////////////////////////////////
  else if(tryb == 1 && power == 1){////////////////////////////////// SOLID
      pixels.setBrightness(255);
      for (int i = 0; i < n; i++) {
        pixels.setPixelColor(i, pixels.Color(R, G, B));
      }
  }/////////////////////////////////////////////////////////////////
  else if(tryb == 2 && power == 1){ //////////////////////////////// BOUNCE
    pixels.setBrightness(255);
    if(millis() - t_time > (250 - (s * 2))){
      t_time = millis();
      if(dir == 0) {
        shift_led ++;
        if(shift_led > n){
          shift_led = n;
          shift_led2 ++;
          if(shift_led2 == n - 1){
            dir = 1;
          }
        }
      }
      else if(dir == 1) {
        shift_led --;
        if(shift_led == 0){
          shift_led = 1;
          shift_led2 --;
          if(shift_led2 == 1){
            dir = 0;
          }
        }
      }
    }
    if(dir == 0) {
      for (int i = 0; i < shift_led; i++) {
        pixels.setPixelColor(i, pixels.Color(R, G, B));
      }
      for (int i = 0; i < shift_led2; i++) {
        pixels.setPixelColor(i, pixels.Color(0, 0, 0));
      }
    }else {
      for (int i = n - 1; i > shift_led; i--) {
        pixels.setPixelColor(i, pixels.Color(R, G, B));
      }
      for (int i = n - 1; i > shift_led2; i--) {
        pixels.setPixelColor(i, pixels.Color(0, 0, 0));
      }
    }   
  }/////////////////////////////////////////////////////////////
  else if(tryb == 3 && power == 1){ //////////////////////////// BREATH
    pixels.setBrightness(90 + sin(help) * 85);
    for (int i = 0; i < n; i++) {
      pixels.setPixelColor(i, pixels.Color(R, G, B));
    }
    help += 0.025 + (s / 1000.0);
    if(help > 2 * PI) help = 0;
  }//////////////////////////////////////////////////////////////
  pixels.show();
}

void setup() {
# if defined (__AVR_ATtiny85__)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  pixels.begin();
  pixels_lcd.begin();

  for (int i = 0; i < NUMPIXELS_LCD; i++) {
    pixels_lcd.setPixelColor(i, pixels.Color(0, 0, 0));
  }
  pixels_lcd.show();
  Serial.begin(115200);
}

void loop() {
  readSerial();
}
