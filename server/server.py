import socket
import sys
import threading
import pickle

class Server():

    clientSockets = []

    clientAlias = []

    def __init__(self, host='localhost', port=5000, listens=10):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (str(host), int(port))
        self.sock.bind(server_address)
        self.sock.listen(int(listens))
        self.sock.setblocking(False)

        accept = threading.Thread(target=self.acceptConnection)
        # close = threading.Thread(target=self.closeConnection) 

        accept.daemon = True
        # close.daemon = True

        accept.start()
        # close.start()

        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print("Hostname: " + hostname)
        print("IP: " + local_ip)

        while True:
            msg = input('->')
            if msg == 'salir':
                self.sock.close()
                sys.exit()

    def acceptConnection(self):
        print("aceptar conexión")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clientSockets.append(conn)
                # if len(self.clientSockets) > 0:
                for c in self.clientSockets:
                    try:
                        data = c.recv(1024) #localhost:127.0.0.1
                        if data: 
                            self.clientAlias.append(data)
                            self.msg_to_all(self.clientAlias)
                    except:
                        pass
            except: 
                pass
    
    def msg_to_all(self, msg):
        for i, c in enumerate(self.clientSockets):
            try:
                c.send(pickle.dumps(msg))
            except:
                del self.clientAlias[i]
                self.clientSockets.remove(c)


s = Server('localhost', 5000)