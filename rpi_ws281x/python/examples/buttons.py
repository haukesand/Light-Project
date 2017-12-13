import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

button_start = 11
button_stop = 10
button_light = 9
button_help = 8

GPIO.setup(button_start, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_light, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_help, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO.wait_for_edge(button_start, GPIO.FALLING)
#print "falling"

while True:
	print GPIO.input(button_stop)
	print GPIO.input(button_light)
	print GPIO.input(button_help)
	print GPIO.input(button_start)

