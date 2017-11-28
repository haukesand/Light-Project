# Adapted from Abraboxabra 1.0 Piero

from bluetooth import *
import animation
import send
#import threading
import time
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
    client_sock, client_info = server_sock.accept()
    print ("Accepted Bluetooth connection from ", client_info)
    sendNow = send.Send(drawNow)


    while True:
        try:
            data = client_sock.recv(1024)
            print("received command %s" % data)
            if data.startswith('<') and data.endswith('>'):
                light_type, always_loop, loop_time, loop_amount, strength, angle = [None] * 6
                splitted = data[1:-1].split(',')
                light_type = splitted[0]
                for item in splitted[1:]:
                    if item.startswith('loop'):
                        loop_value = item[5:]
                        if "." in loop_value:
                            loop_time = loop_value
                        elif loop_value == "INF":
                            always_loop = True
                        elif loop_value == "OFF":  # turn the animation off
                            drawNow.off_animation(light_type=light_type)
                            always_loop = False
                            break
                        else:
                            loop_amount = loop_value
                        drawNow.new_animation(light_type=light_type, always_loop=always_loop, loop_time=loop_time, loop_amount=loop_amount,
                                              strength = strength, angle=angle)
                    elif item.startswith('strength'):
                        strength = item[9:]
                        drawNow.new_animation(light_type=light_type, always_loop=always_loop, loop_time=loop_time, loop_amount=loop_amount,
                                              strength = strength, angle=angle)
                    elif item.startswith('angle'):
                        angle = item[6:]
                        drawNow.new_animation(light_type=light_type, always_loop=always_loop, loop_time=loop_time, loop_amount=loop_amount,
                                              strength = strength, angle=angle)
                if always_loop is not False:
                    drawNow.new_animation(light_type=light_type, always_loop=always_loop, loop_time=loop_time, loop_amount=loop_amount, strength = strength, angle=angle)
                else:
                    drawNow.off_animation(light_type=light_type)

        except IOError:
            client_sock, client_info = server_sock.accept()
            print("Accepted Bluetooth connection from ", client_info)
            pass

    client_sock.close()
    server_sock.close()

except KeyboardInterrupt:
    drawNow.stop()
    sendNow.stop()
    print "\nInterrupted from Keyboard interrupt in receive"
    pass
