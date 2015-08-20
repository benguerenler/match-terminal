
import socket
import json
import random

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

    def post(self):
        # Tell the server p
        self.socket.sendall("p")
        self.socket.sendall(self.userid)

        message = raw_input("Write your message: ")
        amount = raw_input("amount to charge: ")
        deadline = raw_input("deadline: ")
        cancellable = raw_input("cancellable? [Y/n]")
        servid = random.randint(1, 1000000)
        data = json.dumps({"serviceid": servid, "message": message, "amount": amount, "deadline": deadline, "cancellable": cancellable})

        self.socket.sendall(data)

    def pending(self):
        pass

    def list_all(self):
        pass

    def start(self):
        self.socket.connect(("", 8888))
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
                  "[p] Post a new service\n" \
                  "[r] Read your pending requests\n" \
                  "[l] list all\n" \
                  "[x] Exit"

            option = raw_input()
            if option == "x": self.exit()
            elif option == "p": self.post()
            elif option == "r": self.pending()
            elif option == "l": self.list_all()
            else: pass


if __name__ == "__main__":
    client = Client()
    client.start()
