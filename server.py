import socket
import sys
import threading
import json
from db import Database
from models import Service
from config import HOST, PORT


class Server(object):

    def __init__(self):
        self.db = Database()

    def socket_dance(self, conn):
        try:
            conn.send("Connected to server. Please enter your id first")

            # Be polite Server!
            while True:
                id_user = conn.recv(1024)
                if self.db.user(id_user):
                    break
                else:
                    print "Please try again"

            reply = "Hi " + self.db.user(id_user).name
            self.db.user(id_user).conn = conn
            conn.sendall(reply)

            while (True):
                option = conn.recv(1)
                if option == "p": self.post(conn)
                elif (option == "l"): self.list_all(conn)
                else: pass

        except socket.error as err:
            pass

    def post(self, conn):
        data = json.loads(conn.recv(1024))
        service = Service(**data)
        self.db.services.append(service)
        print "Request: '%s', %s received from user %s" % (service.short_message, service.amount, service.requester)


    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind socket to localhost and port
        try:
            s.bind((HOST, PORT))
        except socket.error as msg:
            print 'Bind failer. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        print 'Socket bind complete'

        # listen on socket
        s.listen(10)
        print 'Socket listening'

        while True:
            conn, addr = s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            t = threading.Thread(target=self.socket_dance, args=(conn,))
            t.start()


if __name__ == "__main__":
    server = Server()
    server.start()
