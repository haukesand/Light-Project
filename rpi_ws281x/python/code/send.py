
# run with: sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python examples/multistrandtest2image.py

import time
import numpy as np
import gizeh as gz
import imageio
import threading
from neopixel import *
from itertools import *

# LED strip configuration:
LED_1_COUNT = 120      # Number of LED pixels.
# GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_PIN = 13
LED_1_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
# DMA channel to use for generating signal (Between 1 and 14)
LED_1_DMA = 5
LED_1_BRIGHTNESS = 20     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_1_INVERT = False
LED_1_CHANNEL = 1       # 0 or 1
LED_1_STRIP = ws.SK6812_STRIP_GRBW

LED_2_COUNT = 120      # Number of LED pixels.
# GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_PIN = 12
LED_2_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
# DMA channel to use for generating signal (Between 1 and 14)
LED_2_DMA = 10
LED_2_BRIGHTNESS = 20     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_2_INVERT = False
LED_2_CHANNEL = 0       # 0 or 1
LED_2_STRIP = ws.SK6812_STRIP_GRBW

duration = 2  # duration of the clip, in seconds

class Send(object):
    def __init__(self, animation):
        self.H,self.W = 90,78
        self.position = 0
        self.surface = gz.Surface(self.W,self.H, bg_color=(0,0,0))
        self.radius = 50
        self.t = 0
        # Create NeoPixel objects with appropriate configuration for each strip.
        self.strip1 = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ,
                                   LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL, LED_1_STRIP)
        self.strip2 = Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ,
                                   LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL, LED_2_STRIP)
        self._is_running = True
        self.animation = animation

        thread = threading.Thread(target=self.send, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        
    
    def send(self):
        # Intialize the library (must be called once before other functions).
        self.strip1.begin()
        self.strip2.begin()
        self.blackout(self.strip1, self.strip2)
        print ('Press Ctrl-C to quit.')

        # settuppixel
        imMap = imageio.imread('assets/240RGB.png')  # imMap = np.int_(imMap)
        # Mask the Map and False to work in place
        maMap = np.ma.masked_where(imMap > 240, imMap, False)


        while (self._is_running):
            # Mapcolours
            # imDraw = self.make_frame(self.t)
            # self.t += 0.06
            # if self.t > duration:
            #     self.t = 0
            imDraw = self.animation.get_last_frame()    
            maDraw = np.ma.masked_where(np.ma.getmask(maMap), imDraw, False)

            # remove any additional g & b information but keep dimensionality
            maMapDraw = np.ma.concatenate((maMap[:, :, [0]], maDraw), axis=2)
            compMapDraw = maMapDraw.compressed()  # remove masked values
            iterCMP = grouper(4, compMapDraw, 0)  # turn into iterable chunks

            for data in iterCMP:
                id = data[0]
                r = data[1]
                b = data[2]
                g = data[3]
                if id <= 120:
                    self.strip2.setPixelColor(int(id), Color(r, b, g))
                else:
                    self.strip1.setPixelColor(120 - (id - 120), Color(r, b, g))
                # print "id: {0} r: {1} b: {2} g: {3}".format(id, r, b, g)
            self.strip1.show()
            self.strip2.show()
        

    def stop(self):
        self._is_running = False
        self.blackout(self.strip1, self.strip2)
        print "\nStopped sending"

    def blackout(self, strip1, strip2):
        for i in range(LED_1_COUNT):
            strip1.setPixelColor(i, Color(0, 0, 0))
        for i in range(LED_2_COUNT):
            strip2.setPixelColor(i, Color(0, 0, 0))
        strip1.show()
        strip2.show()

    def make_frame(self, t):
        surface = gz.Surface(self.W, self.H, bg_color=(0, 0, 0))
        speed = self.H * ((t * (duration - t))**3) / 4

        gradient = gz.ColorGradient(type="radial",
                                    stops_colors=[(0, (1, .8, 0)), (1, (0, 0, 0))], xy1=[0, 0], xy2=[0, 0], xy3=[0, self.W / 2])
        circle = gz.circle(r=self.W / 2, fill=gradient).translate(xy=(0, speed - 15))
        circle.draw(self.surface)

        # ellipse = gz.ellipse(self.W, self.H, xy=(self.W / 2, self.H / 2),
        #                     stroke_width=1, stroke=(1, 1, 1))
        # ellipse.draw(self.surface)
        # self.surface.write_to_png("assets/draw.png")
        return self.surface.get_npimage()

def grouper(n, iterable, fillvalue=None):
        "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)