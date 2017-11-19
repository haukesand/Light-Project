# Adapted from Abraboxabra 1.0 Piero

import time
from bluetooth import *

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ],
#                   protocols = [ OBEX_UUID ]
                  )

print ("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print ("Accepted Bluetooth connection from ", client_info)

while True:
   try:
        data = client_sock.recv(1024)
        print("received command %s" % data)
        if data == 'openclose':
                

   except IOError:
      client_sock, client_info = server_sock.accept()
      print("Accepted Bluetooth connection from ", client_info)
      pass

