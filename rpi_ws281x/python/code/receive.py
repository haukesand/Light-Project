# Adapted from Abraboxabra 1.0 Piero

from bluetooth import *
import animation
import send
# import RPi.GPIO as GPIO
import time
import threading
# import i2c_display as display

# Setup the buttons
# GPIO.setmode(GPIO.BCM)

button_start = 11
button_stop = 8
button_light = 9
button_help = 10

shutdown_count = 0
restart_count = 0

def poweroff():
    command = "/usr/bin/sudo /sbin/shutdown -P now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

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

    client_sock, client_info = server_sock.accept()
    print ("Accepted Bluetooth connection from ", client_info)

    while True:
        try:
            data = client_sock.recv(1024)
            print("received command %s" % data)

            if data.startswith('<') and data.endswith('>') and not ">" in data[1:-1]:
                if data[1:-1].startswith('Custom,'):
                    # custom light signal definition
                    if data[8:-1].startswith('type='):
                        drawNow.custom_animation(data[13:-1])
                    elif data[8:-1].startswith('size='):
                        drawNow.update_ca(size=data[13:-1])
                    elif data[8:-1].startswith('duration='):
                        drawNow.update_ca(size=data[17:-1])
                    elif data[8:-1].startswith('angle='):
                        drawNow.update_ca(size=data[14:-1])
                    elif data[8:-1].startswith('direction='):
                        drawNow.update_ca(size=data[18:-1])
                    elif data[8:-1].startswith('color='):
                        splitted = data[14:-1].split(',')
                        drawNow.color_ca(R=float(splitted[0]),G=float(splitted[1]),B=float(splitted[2]),A=float(splitted[3]))

                else:
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
                        elif item.startswith('angle'):
                            angle = float(item[6:])
                    if light_type != "light_up" and light_type != "idle":
                        # print light_type
                        if always_loop is not False or always_loop is None:
                            drawNow.new_animation(light_type=light_type, always_loop=always_loop,
                                                  loop_time=loop_time, loop_amount=loop_amount, strength=strength, angle=angle)
                        else:
                            drawNow.off_animation(light_type=light_type)
                    else:
                        drawNow.set_light(light_type, always_loop)

        except IOError:
            client_sock, client_info = server_sock.accept()
            print("Accepted Bluetooth connection from ", client_info)
            pass

    client_sock.close()
    server_sock.close()

except KeyboardInterrupt:
    sendNow.stop()
    drawNow.stop()
    print "\nInterrupted from Keyboard interrupt in receive"
    pass
