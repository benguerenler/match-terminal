
import socket
from config import HOST, PORT


class ABCClient(object):

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._userid = None

    @property
    def userid(self):
        return self._userid

    @userid.setter
    def userid(self, value):
        self._userid = value

    def exit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def start(self):
        self.socket.connect((HOST, PORT))
        data = self.socket.recv(1024)
        print data

        # Enter id
        while True:
            self.userid = raw_input("> ")
            if self.userid != "":
                self.socket.sendall(self.userid)
                break
            else: print "Try again\n"

        # receive greeting
        print "\n" + self.socket.recv(1024)