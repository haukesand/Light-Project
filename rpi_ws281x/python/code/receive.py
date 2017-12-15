# Adapted from Abraboxabra 1.0 Piero

from bluetooth import *
import animation
import send
import RPi.GPIO as GPIO
import time
import threading
# Setup the buttons

# from tendo import singleton
# me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

GPIO.setmode(GPIO.BCM)

button_start = 11
button_stop = 8
button_light = 9
button_help = 10

shutdown_count = 0

GPIO.setup(button_start, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_light, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_help, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def poweroff():
    command = "/usr/bin/sudo /sbin/shutdown -P now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

def my_callback_button_stop(channel):

    print('Callback button_stop')
    global shutdown_count
    drawNow.new_animation(light_type="swerve_left",  loop_amount=20, always_loop=None)
    shutdown_count += 1
    if shutdown_count > 3:
        poweroff()

def my_callback_button_start(channel):
    print('Callback button_start')
    drawNow.new_animation(light_type="depart_todestination", loop_amount=2, always_loop=None)

def my_callback_button_light(channel):
    drawNow.toggle_user_light()
    print('Callback button_light')

def my_callback_button_help(channel):
    drawNow.toggle_augmentation_on()
    print('Callback button_help')


# Setup the bluetooth connection
server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service(server_sock, "SampleServer",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
                  #                   protocols = [ OBEX_UUID ]
                  )

print ("Waiting for connection on RFCOMM channel %d" % port)
try:

    drawNow = animation.Draw()
    sendNow = send.Send(drawNow)

    GPIO.add_event_detect(button_start, GPIO.FALLING, callback=my_callback_button_start, bouncetime=1500)
    GPIO.add_event_detect(button_stop, GPIO.FALLING, callback=my_callback_button_stop, bouncetime=1500)
    GPIO.add_event_detect(button_light, GPIO.FALLING, callback=my_callback_button_light, bouncetime=1500)
    GPIO.add_event_detect(button_help, GPIO.FALLING, callback=my_callback_button_help, bouncetime=1500)

    client_sock, client_info = server_sock.accept()
    print ("Accepted Bluetooth connection from ", client_info)

    while True:
        try:
            data = client_sock.recv(1024)
            print("received command %s" % data)

            if data.startswith('<') and data.endswith('>'):
                light_type, always_loop, loop_time, loop_amount, strength, angle = [
                    None] * 6
                splitted = data[1:-1].split(',')
                light_type = splitted[0]
                # display.write_line(1, light_type)
                for item in splitted[1:]:
                    if item.startswith('loop'):
                        loop_value = item[5:]
                        if "." in loop_value:
                            loop_time = float(loop_value)
                        elif loop_value == "INF":
                            always_loop = True
                        elif loop_value == "OFF":  # turn the animation off
                            drawNow.off_animation(light_type=light_type)
                            always_loop = False
                            break
                        elif loop_value == "ONE":  # turn the animation off
                            loop_amount = 1
                        else:
                            loop_amount = int(loop_value)
                    elif item.startswith('strength'):
                        strength = float(item[9:])
                        drawNow.new_animation(light_type=light_type, always_loop=always_loop, loop_time=loop_time, loop_amount=loop_amount,
                                              strength = strength, angle=angle)
                    elif item.startswith('angle'):
                        angle = float(item[6:])
                        drawNow.new_animation(light_type=light_type, always_loop=always_loop, loop_time=loop_time, loop_amount=loop_amount,
                                              strength = strength, angle=angle)
                if light_type != "light_up":
                    print light_type
                    if always_loop is not False or always_loop is None:
                        drawNow.new_animation(light_type=light_type, always_loop=always_loop,
                                              loop_time=loop_time, loop_amount=loop_amount, strength=strength, angle=angle)
                    else:
                        drawNow.off_animation(light_type=light_type)
                else:
                    drawNow.set_light(always_loop)

        except IOError:
            client_sock, client_info = server_sock.accept()
            print("Accepted Bluetooth connection from ", client_info)
            pass

    client_sock.close()
    server_sock.close()

except KeyboardInterrupt:
    sendNow.stop()
    drawNow.stop()
    GPIO.remove_event_detect(button_start)
    GPIO.cleanup()
    print "\nInterrupted from Keyboard interrupt in receive"
    pass
