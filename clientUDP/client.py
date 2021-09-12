import socket
import time
import sys
import os


UDP_IP = "192.168.1.76"
UDP_PORT = 4444
buf = 1024 * 4
file_name = sys.argv[1]
SEPARATOR = "<SEPARATOR>"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.sendto(file_name.encode('utf-8'), (UDP_IP, UDP_PORT))
filesize = os.path.getsize(file_name)
sock.sendto(f"{file_name}{SEPARATOR}{filesize}".encode(), (UDP_IP, UDP_PORT))
#print "Sending %s ..." % file_name

filesize = os.path.getsize(file_name)

with open(file_name, "rb") as f:
    while True:                
        bytes_read = f.read(buf)
        if not bytes_read:                    
            break
        
        sock.sendto(bytes_read, (UDP_IP, UDP_PORT))

sock.close()

f = open(file_name, encoding="utf8")
data = f.read(buf)
while(data):
    if(sock.sendto(data.encode('utf-8'), (UDP_IP, UDP_PORT))):
        data = f.read(buf)
        time.sleep(0.02) # Give receiver a bit time to save

sock.close()
f.close()