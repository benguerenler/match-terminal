import socket
import random
import json
from datetime import datetime
from config import HOST, PORT
from models import Service

def validate_datetime(d):
    try:
        datetime.strptime(d, "%Y-%m-%d")
        return True
    except ValueError:
        return False

class Requester(object):
    MESSAGE = 1
    PRICE = 2
    CANCELLABLE = 3
    DEADLINE = 4

    INFO = {MESSAGE: "Write your message",
            PRICE: "Payment (SEK)",
            CANCELLABLE: "Can it be cancelled if there are not enough people? [Y/n]",
            DEADLINE: "Date for the deadline (format: YYYY-MM-DD)"}

    VALIDATOR = {MESSAGE: lambda x: x != "",
                 PRICE: lambda x: x.isdigit(),
                 CANCELLABLE: lambda x: x in ("Y", "Yes", "y", "N", "n", "no"),
                 DEADLINE: validate_datetime }


    def __init__(self, *args, **kwargs):
        super(Requester, self).__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._userid = None

    @property
    def userid(self):
        return self._userid

    @userid.setter
    def userid(self, userid):
        self._userid = userid

    def exit(self):
        self.socket.shutdown(1)
        self.socket.close()

    def validate(func):
        def _decorator(this, kind):
            data = func(this, kind)
            validator = Requester.VALIDATOR.get(kind)
            if validator(data):
                return data
            else:
                return _decorator(this, kind)
        return _decorator

    @validate
    def get_input(self, kind):
        return raw_input(Requester.INFO.get(kind) + ":")

    def post(self):
        # Tell the server p
        self.socket.sendall("p")

        # Fetch service information from requester
        message = self.get_input(Requester.MESSAGE)
        amount = self.get_input(Requester.PRICE)
        deadline = self.get_input(Requester.DEADLINE)
        cancellable = self.get_input(Requester.CANCELLABLE)
        servid = random.randint(1, 1000000)

        # Create service object
        data = Service(message=message, amount=amount, deadline=deadline, cancellable=cancellable, serviceid=servid)
        self.socket.sendall(data.to_json())



    def start(self):
        self.socket.connect((HOST, PORT))
        print self.socket.recv(1024)

        # Enter id
        # TODO: Add validation
        self.userid = raw_input("> ")
        self.socket.sendall(self.userid)

        # receive greeting
        print "\n" + self.socket.recv(1024)

        while True:
            print "\nPlease use one of the following commands to:\n" \
                  "[p] Post a new service\n" \
                  "[r] Read your services\n"\
                  "[l] list all\n" \
                  "[x] Exit\n"

            option = raw_input("> ")
            if option == "x": self.exit()
            elif option == "p": self.post()
            elif option == "l": self.list_all()
            else: pass

if __name__ == "__main__":
    requester = Requester()
    requester.start()
