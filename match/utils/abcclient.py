import socket

from config import HOST, PORT
from backend.db import Database


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
        print self.socket.recv(1024)

        # Enter id
        valid = False
        while not valid:
            userid = raw_input("> ")
            if not userid.isdigit():
                print "the id you typed is not a digit"
            elif Database().user(userid) is None:
                print "there is no user in the database with id %s" % self.userid
            else:
                self.userid = userid
                valid = True

        self.socket.sendall(self.userid)
        # receive greeting
        print "\n" + self.socket.recv(1024)