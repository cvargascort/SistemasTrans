import socket
import sys
import threading
import pickle
import argparse
import os
import tqdm
import threading

SERVER_HOST="192.168.1.76"

SERVER_RECEIVER_PORT=5001
SERVER_SENDER_PORT=5002

SERVER_RECEIVER_MESSAGE_PORT=5003
SERVER_SENDER_MESSAGE_PORT=5004

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4

class Client():
    def __init__(self, host="localhost", port=5000):
        self.reportConnection(host, port)

        receiverMessage = threading.Thread(target=self.receiverFileSocket)
        receiverFile = threading.Thread(target=self.receiverMessageSocket)
        
        receiverMessage.daemon = True
        receiverFile.daemon = True

        receiverMessage.start()
        receiverFile.start()


        while True:
            msg = input("->")
            if msg == 'audio':
                print("Se va a enviar el audio")
                self.send_file("music.mp3")
            elif msg != 'salir':
                self.msg_send(msg)
            else:
                self.sock.close()
                sys.exit()

    def send_file(self, filename):
        
        filesize = os.path.getsize(filename)
        
        s = socket.socket()
        print(f"[+] Connecting to {SERVER_HOST}:{SERVER_SENDER_PORT}")
        s.connect((SERVER_HOST, SERVER_SENDER_PORT))
        print("[+] Connected.")

        
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    
                    break
                
                s.sendall(bytes_read)
                
                progress.update(len(bytes_read))

        
        s.close()

    def receiverMessageSocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((SERVER_HOST, SERVER_RECEIVER_MESSAGE_PORT))
        s.listen(10)
        while True:
            client_socket, address = s.accept() 
            received = client_socket.recv(2048)
            print(received)

            msg = input("->")
            if msg != 'salir':
                s.close()

    def receiverFileSocket(self):

        s = socket.socket()
        s.bind((SERVER_HOST, SERVER_RECEIVER_PORT))
        s.listen(10)

        while True:
            print(f"[*] Listening as {SERVER_HOST}:{SERVER_RECEIVER_PORT}")
            client_socket, address = s.accept() 
            print(f"[+] {address} is connected.")

            received = client_socket.recv(BUFFER_SIZE).decode()

            filename, filesize = received.split(SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)

            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

            with open(filename, "wb") as f:
                while True:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:    
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))

            action = input("->")
            if action == 'salir':
                client_socket.close()
                s.close()

    def reportConnection(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (str(host), int(port))
        print('conectando a {} puerto {}'.format(*server_address))
        self.sock.connect(server_address)
        #hilo que recibe los mensajes que tiene como target una funcion del mismo nombre
        msg_resv = threading.Thread(target=self.msg_resv)
        
        #para que al cerrar elprograma este hilo se muera
        msg_resv.daemon = True

        #correr hilo
        msg_resv.start()

        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        alias = hostname + ":" + local_ip
        self.sock.send(pickle.dumps(alias))

    def msg_resv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    print(pickle.loads(data))
            except:
                pass

    # def msg_send(self, msg):
    #     s = socket.socket()
    #     print(f"[+] Connecting to {SERVER_HOST}:{SERVER_SENDER_PORT}")
    #     s.connect((SERVER_HOST, SERVER_SENDER_PORT))
    #     print("[+] Connected.")
    #     s.send(b"msg".encode())
    #     s.close()

    def msg_send(self, msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[+] Connecting to {SERVER_HOST}:{SERVER_SENDER_MESSAGE_PORT}")
        s.connect((SERVER_HOST, SERVER_SENDER_MESSAGE_PORT))
        print("[+] Connected.")
        s.send(bytes(msg, 'utf-8'))
        s.close()



c = Client('127.0.0.1', 5000)