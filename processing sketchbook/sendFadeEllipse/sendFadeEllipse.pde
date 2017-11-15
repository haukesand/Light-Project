import processing.serial.*;
//Counter
int posx, posy = 0;
int startMillis = 0;

//Data Holder
byte[] sendData = new byte[242];
String ready;
// Constants
int waitMillis = 10;
int Y_AXIS = 1;
int X_AXIS = 2;
int lookUpSizeX = 78;
int lookUpSizeY = 90;
color b1 = color(252);
color b2 = color(0);
PImage lookUpImage;


Serial myPort;  // Create object from Serial class

void setup() {
  size(78, 90);
  background(0);
  frameRate(200);

  lookUpImage = loadImage("240Count.png");

  startMillis = millis();

  //Serial Port
  printArray(Serial.list());
  String portName = Serial.list()[0]; 
  myPort = new Serial(this, portName, 115200); // Uncomment to enable serial connection
}

void draw() {

  int currentMillis = millis();
  if (currentMillis - startMillis > waitMillis)
  {
    //paint animation

    animate();
    mapIt();
    
    ready = myPort.readStringUntil('\n');
    //println(ready);
    if (ready != null) {
          ready = ready.trim();
     if  (ready.equals("OK")){
    sendToSerial();}
    }

    startMillis = currentMillis;
  }//endof millis timer
}
void mapIt()
{

  lookUpImage.loadPixels(); 
  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      int loc = x + y*width;

      float r = red(lookUpImage.pixels[loc]);
      //float g = green(lookUpImage.pixels[loc]);
      //float b = blue(lookUpImage.pixels[loc]);

      if (r!=255) {
        color a = color(get(x, y));
        sendData[int(r+1)] = byte(blue(a)); 

        set(x, y,color(0,0,0));
      }
    }
  }
}

void sendToSerial()
{
  //make sure before sending that start & stop byte are transmitted
  sendData[0] = byte(253); 
  sendData[241] = byte(254); 
  print(sendData);
  saveBytes("numbers.dat", sendData);

  myPort.write(sendData);
}
void animate() {
  background(0);
  setGradient(posx-width/2, 0, width/2, height, b1, b2, X_AXIS);
  setGradient(posx-width, 0, width/2, height, b2, b1, X_AXIS);

  posx++;
  if (posx >= width*2)
  { 
    posx =0;
  }
}

void setGradient(int x, int y, float w, float h, color c1, color c2, int axis ) {

  noFill();

  if (axis == Y_AXIS) {  // Top to bottom gradient
    for (int i = y; i <= y+h; i++) {
      float inter = map(i, y, y+h, 0, 1);
      color c = lerpColor(c1, c2, inter);
      stroke(c);
      line(x, i, x+w, i);
    }
  } else if (axis == X_AXIS) {  // Left to right gradient
    for (int i = x; i <= x+w; i++) {
      float inter = map(i, x, x+w, 0, 1);
      color c = lerpColor(c1, c2, inter);
      stroke(c);
      line(i, y, i, y+h);
    }
  }
}    