import socket
import sys
import threading
import pickle


class Client():
    def __init__(self, host="localhost", port=5000):
        self.reportConnection(host, port)
        while True:
            msg = input("->")
            if msg != 'salir':
                self.msg_send(msg)
            else:
                self.sock.close()
                sys.exit()


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
        self.msg_send(alias)

    def msg_resv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    print(pickle.loads(data))
            except:
                pass

    def msg_send(self, msg):
        self.sock.send(pickle.dumps(msg))



c = Client('127.0.0.1', 5000)