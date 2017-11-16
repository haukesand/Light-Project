#run with: sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python examples/multistrandtest2image.py

import time
import numpy as np
import gizeh as gz
import imageio
from neopixel import *
from itertools import *

# LED strip configuration:
LED_1_COUNT      = 120      # Number of LED pixels.
LED_1_PIN        = 13      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA        = 5       # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 20     # Set to 0 for darkest and 255 for brightest
LED_1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL    = 1       # 0 or 1
LED_1_STRIP      = ws.SK6812_STRIP_GRBW

LED_2_COUNT      = 120      # Number of LED pixels.
LED_2_PIN        = 12      # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 20     # Set to 0 for darkest and 255 for brightest
LED_2_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_2_CHANNEL    = 0       # 0 or 1
LED_2_STRIP      = ws.SK6812_STRIP_GRBW


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def blackout(strip1, strip2):
	for i in range(LED_1_COUNT):
		strip1.setPixelColor(i, Color(0,0,0))
	for i in range(LED_2_COUNT):
		strip2.setPixelColor(i, Color(0,0,0))
	strip1.show()
	strip2.show()


# Main program logic follows:
if __name__ == '__main__':
        ##SETUPPIXEL
    	# Create NeoPixel objects with appropriate configuration for each strip.
    	strip1 = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL, LED_1_STRIP)
    	strip2 = Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL, LED_2_STRIP)

    	# Intialize the library (must be called once before other functions).
    	strip1.begin()
    	strip2.begin()
        blackout(strip1,strip2)
    	print ('Press Ctrl-C to quit.')

    	##settuppixel
    	imMap = imageio.imread('assets/240RGB.png') #imMap = np.int_(imMap)
    	maMap = np.ma.masked_where(imMap > 240, imMap, False)#Mask the Map and False to work in place

    	L,W = 90,78
    	position = 0
    	surface = gz.Surface(W,L, bg_color=(0,0,0))
    	radius = 50

    	centers = [ gz.polar2cart(40, angle) for angle in [0, 2*np.pi/3, 4*np.pi/3]]
    	colors = [ (1,0,0,.4), # <- Semi-tranparent red (R,G,B, transparency)
    			   (0,1,0,.4), # <- Semi-tranparent green
    			   (0,0,1,.4)] # <- Semi-tranparent blue

    	circles = gz.Group( [ gz.circle(radius, xy=center, fill=color,
    									stroke_width=0, stroke=(0,0,0)) # black stroke
    						  for center, color in zip(centers, colors)] )
    	try:
            while True:
    		circles.translate([W/2,position]).draw(surface)
    		position += 1
    		if position > L :
    			position = 0

    		#surface.write_to_png("assets/draw.png")

    		#Mapcolours
    		imDraw = surface.get_npimage(False)#imDraw = imageio.imread('assets/draw.png')
    		maDraw = np.ma.masked_where(np.ma.getmask(maMap), imDraw, False)

    		maMapDraw = np.ma.concatenate((maMap[:,:,[0]], maDraw), axis=2)#remove any additional g & b information but keep dimensionality
    		compMapDraw = maMapDraw.compressed()#remove masked values
    		iterCMP = grouper(4, compMapDraw, 0)#turn into iterable chunks

    		for data in iterCMP:
    			id = data[0]
    			r = data[1]
    			b = data[2]
    			g = data[3]
    			if id <= 120:
    				strip2.setPixelColor(int(id), Color(r, b, g))
    			else:
    				strip1.setPixelColor(120-(id-120), Color(r, b, g))
    			#print "id: {0} r: {1} b: {2} g: {3}".format(id, r, b, g)
    		strip1.show()
    		strip2.show()
    	except KeyboardInterrupt:
            blackout(strip1,strip2)
            print "\nInterrupted"
    		#time.sleep(1)
