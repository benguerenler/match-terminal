import json
from datetime import datetime

from utils import config
from backend import db
from backend.models import Request
from utils.abcclient import ABCClient
from utils import decorator


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

    INFO = {MESSAGE: "Enter textual description",
            PRICE: "How much will you pay",
            CANCELLABLE: "Can it be cancelled if there are not enough people? [Y/n]",
            DEADLINE: "Date for the deadline (format: YYYY-MM-DD)"}

    VALIDATOR = {MESSAGE: lambda x: x != "",
                 PRICE: lambda x: x.isdigit(),
                 CANCELLABLE: lambda x: x in ("Y", "Yes", "y", "N", "n", "no"),
                 DEADLINE: validate_datetime}

    def __init__(self, *args, **kwargs):
        super(Requester, self).__init__(*args, **kwargs)

    @decorator.validate
    def get_input(self, kind):
        print Requester.INFO.get(kind) + ":"
        return raw_input("> ")

    def post(self):
        # Tell the server p
        self.socket.sendall("p")

        # Fetch service information from requester
        message = self.get_input(Requester.MESSAGE)
        amount = self.get_input(Requester.PRICE)
        deadline = self.get_input(Requester.DEADLINE)
        cancellable = self.get_input(Requester.CANCELLABLE)
        requestid = db.inc_request_counter()

        # Create service object
        data = Request(message=message, amount=amount, deadline=deadline, cancellable=cancellable,
                       requestid=requestid, requester=self.userid)
        self.socket.sendall(json.dumps(data.formatting()))
        print "Request posted to Match system"

    def list_all(self):
        self.socket.sendall("l")

        data = self.socket.recv(config.POST_SIZE)
        requests = [Request(**request) for request in json.loads(data)]
        print "Listing all requests"
        for request in requests:
            print "-----------------------------------"
            print "Amount to receive: %s\nDescription: %s\nDeadline: %s" % (
                request.amount, request.message, request.deadline)

    def start(self):
        super(Requester, self).start()
        while True:
            print "\nPlease use one of the following commands to:\n" \
                  "[p] Post a new request\n" \
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
