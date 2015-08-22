
import socket
import json
import random
from config import HOST, PORT

class Client:

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
        self.socket.shutdown(1)
        self.socket.close()

    def pending(self):
        pass

    def list_all(self):
        pass

    def start(self):
        self.socket.connect((HOST, PORT))
        data = self.socket.recv(1024)
        print data

        # Enter id
        while True:
            self.userid = raw_input()
            if self.userid != "":
                self.socket.sendall(self.userid)
                break
            else: print "Try again\n"

        # receive greeting
        print self.socket.recv(1024)

        while True:
            print "Please use one of the following commands to:\n" \
                  "[r] Read your pending requests\n" \
                  "[l] list all\n" \
                  "[x] Exit"

            option = raw_input("> ")
            if option == "x": self.exit()
            elif option == "r": self.pending()
            elif option == "l": self.list_all()
            else: pass


if __name__ == "__main__":
    client = Client()
    client.start()
