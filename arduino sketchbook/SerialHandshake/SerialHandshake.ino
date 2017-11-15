#include <Adafruit_NeoPixel.h>

#define NUMPIXELS 240 // Number of LEDs in array
#define PIN 2 // Ardunio data pin
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRBW + NEO_KHZ800);

unsigned long interval=100;
unsigned long previousMillis=0; 
String readyS= "OK\r\n";

const int numChars = 242;
//byte receivedChars[numChars];

boolean newData = false;
    static boolean recvInProgress = false;

void setup() {
    Serial.begin(115200);
    strip.begin();
    strip.show();

      while (!Serial) {
    ; // wait for port to be ready
  }
  
  // Tell the computer that we're ready for data
  Serial.print(readyS);
  previousMillis = millis();

}

void loop() {
    recvWithStartEndMarkers();
    unsigned long currentMillis = millis(); // grab current time
    if ((unsigned long)(currentMillis - previousMillis) >= interval) {
    Serial.print(readyS);
    previousMillis = millis();

    }
    showNewData();
}

void recvWithStartEndMarkers() {
    static byte ndx = 0;
    byte startMarker = 253;
    byte endMarker = 254;
    byte rc;
        

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                //receivedChars[ndx] = rc;
                
                strip.setPixelColor(ndx, strip.Color(0,0,0, rc));
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                //receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void showNewData() {
    while (newData == true) {

        strip.show();

        while (Serial.available() > 0) Serial.read();
        previousMillis = millis();
        Serial.print(readyS);
        newData = false;

    }
}
