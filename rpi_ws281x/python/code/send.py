
# run with: sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python examples/multistrandtest2image.py
import sys
sys.path.append("/home/pi/Light Project/rpi_ws281x/python/build/lib.linux-armv7l-2.7")
import time
import numpy as np
import gizeh as gz
import imageio
import threading
from neopixel import *
from itertools import *
from tendo import singleton
me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running
# LED strip configuration:
LED_1_COUNT = 54      # Number of LED pixels.
# GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_PIN = 18
LED_1_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
# DMA channel to use for generating signal (Between 1 and 14)
LED_1_DMA = 10
LED_1_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_1_INVERT = False
LED_1_CHANNEL = 0       # 0 or 1
LED_1_STRIP = ws.WS2811_STRIP_GRB

class Send(object):
    def __init__(self, animation):
        self.H,self.W = 19,20
        self.position = 0
        self.surface = gz.Surface(self.W,self.H, bg_color=(0,0,0))
        self.radius = 50
        self.t = 0
        self.w = 0
        self.lightFlag = False
        # Create NeoPixel objects with appropriate configuration for each strip.
        self.strip1 = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ,
                                   LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL, LED_1_STRIP)
        
        self._is_running = True
        self.animation = animation

        thread = threading.Thread(name='send', target=self.send, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

        print "Start send thread"


    def send(self):
        # Intialize the library (must be called once before other functions).
        self.strip1.begin()

        print ('Press Ctrl-C to quit.')

        # settuppixel
        imMap = imageio.imread('/home/pi/Light Project/rpi_ws281x/python/assets/54CC_out.png')  # imMap = np.int_(imMap)
        # Mask the Map and False to work in place
        maMap = np.ma.masked_where(imMap > 240, imMap, False)


        while (self._is_running):
            if self.animation.get_light_on() == True and not self.lightFlag:
                self.w = 30
                self.whitein(self.strip1)
                self.lightFlag = True
            elif self.lightFlag and not self.animation.get_light_on():
                self.blackout(self.strip1)
                self.w = 0
                self.lightFlag = False

            imDraw = self.animation.get_last_frame()
            maDraw = np.ma.masked_where(np.ma.getmask(maMap), imDraw, False)

            # remove any additional g & b information but keep dimensionality
            maMapDraw = np.ma.concatenate((maMap[:, :, [0]], maDraw), axis=2)
            compMapDraw = maMapDraw.compressed()  # remove masked values
            iterCMP = grouper(4, compMapDraw, 0)  # turn into iterable chunks

            for data in iterCMP:
                id = data[0]
                r = int(data[1])
                b = int(data[2])
                g = int(data[3])
                w = self.w - r/2 + b/2 + g/2
                w = max(0, min(w, self.w)) # for whatever reason is this maximal a positive uint8
                myColor = Color(r, b, g)
                self.strip1.setPixelColor(int(id), myColor)
               
                # print "id: {0} r: {1} b: {2} g: {3}".format(id, r, b, g)
            self.strip1.show()


    def stop(self):
        self._is_running = False
        self.blackout(self.strip1)
        print "\nStopped sending"
        sys.exit(0)

    def blackout(self, strip1):
        for n in range (self.w):
            w = self.w - n
            for i in range(LED_1_COUNT):
                strip1.setPixelColor(i, Color(150, 150, 150))
            strip1.show()

    def whitein(self, strip1):
        for n in range (self.w):
            w = n
            for i in range(LED_1_COUNT):
                strip1.setPixelColor(i, Color(0, 0, 0, w))
                strip1.show()

        return self.surface.get_npimage()

def grouper(n, iterable, fillvalue=None):
        "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)
