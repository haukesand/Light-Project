PImage img;
int count = 0;
int lastInLine = 0;
PGraphics alphaG;

boolean drawOnce = false;
void setup() {
  size(78, 90);
  img = loadImage("240.png");
  alphaG = createGraphics(width,height, JAVA2D);
 alphaG.beginDraw();

}

void draw() {
  if (!drawOnce){
     alphaG.beginDraw();

  loadPixels(); 
  updatePixels();
  // Since we are going to access the image's pixels too 
  alphaG.loadPixels();
  img.loadPixels(); 
  //top right
  for (int y = 0; y < height/2; y++) {
    for (int x = width/2; x < width; x++) {
      int loc = x + y*width;
      
      // The functions red(), green(), and blue() pull out the 3 color components from a pixel.
      float r = red(img.pixels[loc]);
      float g = green(img.pixels[loc]);
      float b = blue(img.pixels[loc]);
      //float a = alpha(img.pixels[loc]);
      //float a= 255;
    if (r <= 40){
    r=count;
    g=count;
    b=count;
    //a=count;
    count++;
    }
      alphaG.pixels[loc] =  color(r,g,b);          
}
}

    //bottom right
   for (int y = height/2; y < height; y++) {
    for (int x = width-1; x > width/2; x--) {
      int loc = x + y*width;
      
      // The functions red(), green(), and blue() pull out the 3 color components from a pixel.
      float r = red(img.pixels[loc]);
      float g = green(img.pixels[loc]);
      float b = blue(img.pixels[loc]);
      //float a = alpha(img.pixels[loc]);
      //float a= 255;

    if (r <= 40){
    r=count;
    g=count;
    b=count;
//a=count;
    count++;
    }
      alphaG.pixels[loc] =  color(r,g,b);           
    }
  }
  //bottom left
   for (int y = height-1; y > height/2; y--) {
    for (int x = width/2; x >= 0; x--) {

      int loc = x + y*width;
      
      // The functions red(), green(), and blue() pull out the 3 color components from a pixel.
      float r = red(img.pixels[loc]);
      float g = green(img.pixels[loc]);
      float b = blue(img.pixels[loc]);
           // float a = alpha(img.pixels[loc]);
            //float a= 255;

    if (r <= 40){
    r=count;
    g=count;
    b=count;
    //a=count;
    count++;
    }
   alphaG.pixels[loc] =  color(r,g,b);        
}
}
    //top left
   for (int y = height/2; y >=0; y--) {
    for (int x = 0; x < width/2; x++) {

      int loc = x + y*width;
      
      // The functions red(), green(), and blue() pull out the 3 color components from a pixel.
      float r = red(img.pixels[loc]);
      float g = green(img.pixels[loc]);
      float b = blue(img.pixels[loc]);
         //   float a = alpha(img.pixels[loc]);
            //float a= 255;

    if (r <= 40){
    r=count;
    g=count;
    b=count;
   // a=count;
    count++;
    }
   alphaG.pixels[loc] =  color(r,g,b);              
}
}
      println(count);

  count = 0;
  updatePixels();
 image(alphaG, 0,0);

   alphaG.endDraw();
  alphaG.save("240RGB.png");
  drawOnce = true;
  
  
  }
}