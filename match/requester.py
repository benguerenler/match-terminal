import random
import json
from datetime import datetime
from models import Service
from abcclient import ABCClient


def validate_datetime(d):
    try:
        datetime.strptime(d, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class Requester(ABCClient):
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
                 DEADLINE: validate_datetime}

    def __init__(self, *args, **kwargs):
        super(Requester, self).__init__(*args, **kwargs)

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
        data = Service(message=message, amount=amount, deadline=deadline, cancellable=cancellable,
                       serviceid=servid, requester=self.userid)
        self.socket.sendall(json.dumps(data.formatting()))

    def list_all(self):
        self.socket.sendall("l")

        data = self.socket.recv(2048)
        services = [Service(**service) for service in json.loads(data)]
        print "Listing all requests"
        for service in services:
            print "-----------------------------------"
            print "Amount to receive: %s\nDescription: %s\nDeadline: %s" % (
                service.amount, service.message, service.deadline)

    def start(self):
        super(Requester, self).start()
        while True:
            print "\nPlease use one of the following commands to:\n" \
                  "[p] Post a new service\n" \
                  "[r] Read your services\n" \
                  "[l] list all\n" \
                  "[x] Exit\n"

            option = raw_input("> ")
            if option == "x":
                self.exit()
                break
            elif option == "p":
                self.post()
            elif option == "l":
                self.list_all()
            else:
                pass


if __name__ == "__main__":
    requester = Requester()
    requester.start()
