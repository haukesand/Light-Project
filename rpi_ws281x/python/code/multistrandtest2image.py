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
LED_1_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL    = 1       # 0 or 1
LED_1_STRIP      = ws.SK6812_STRIP_GRBW	

LED_2_COUNT      = 120      # Number of LED pixels.
LED_2_PIN        = 12      # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_2_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_2_CHANNEL    = 0       # 0 or 1
LED_2_STRIP      = ws.SK6812_STRIP_GRBW


def walkThrough( wait_ms=5):
	global strip1
	global strip2


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)		
	
def blackout(strip):
	for i in range(max(strip1.numPixels(), strip1.numPixels())):
		strip.setPixelColor(i, Color(0,0,0))
		strip.show()

		
# Main program logic follows:
if __name__ == '__main__':
	##SETUPPIXEL
	# Create NeoPixel objects with appropriate configuration for each strip.
	strip1 = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL, LED_1_STRIP)
	strip2 = Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL, LED_2_STRIP)

	# Intialize the library (must be called once before other functions).
	strip1.begin()
	strip2.begin()

	print ('Press Ctrl-C to quit.')
	
	# Black out any LEDs that may be still on for the last run
	blackout(strip1)
	blackout(strip2)	
	##settuppixel


	L,W = 90,78
	surface = gz.Surface(W,L, bg_color=(0,0,0))
	radius = 50
	centers = [ gz.polar2cart(40, angle) for angle in [0, 2*np.pi/3, 4*np.pi/3]]
	colors = [ (1,0,0,.4), # <- Semi-tranparent red (R,G,B, transparency)
			   (0,1,0,.4), # <- Semi-tranparent green
			   (0,0,1,.4)] # <- Semi-tranparent blue
	
	circles = gz.Group( [ gz.circle(radius, xy=center, fill=color,
									stroke_width=0, stroke=(0,0,0)) # black stroke
						  for center, color in zip(centers, colors)] )

	circles.translate([W/2,L/2]).draw(surface)

	#surface.write_to_png("assets/draw.png")

	#Mapcolours
	imMap = imageio.imread('assets/240RGB.png') #imMap = np.int_(imMap)
	#imDraw = imageio.imread('assets/draw.png')
	imDraw = surface.get_npimage(False)
	
	maMap = np.ma.masked_where(imMap > 240, imMap, False)#Mask the Map and the Draw Canvas
	maDraw = np.ma.masked_where(np.ma.getmask(maMap), imDraw, False)#False to not return a copy but work in place

	maMapDraw = np.ma.concatenate((maMap[:,:,[0]], maDraw), axis=2)#remove any additional g & b information but keep dimensionality

	compMapDraw = maMapDraw.compressed()#remove masked values
	iterCMP = grouper(4, compMapDraw, 0)#turn into iterable chunks
	
	##DRAW
	#while True:
	
	for data in iterCMP:
		
		id = data[0]
		r = data[1]
		b = data[2]
		g = data[3]
		if id <= 120:
			strip1.setPixelColor(int(id), Color(r, b, g))
		else:
			strip2.setPixelColor(120-(int(id)-120), Color(r, b, g))
		#print "id: {0} r: {1} b: {2} g: {3}".format(id, r, b, g)
	strip1.show()
	strip2.show()
	
	time.sleep(1)
		
