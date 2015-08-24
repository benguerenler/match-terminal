from abcclient import ABCClient
from utils import decorator
import db
import models
import json
import config


class Responder(ABCClient):
    ACCEPT_OR_DECLINE = 1

    INFO = {ACCEPT_OR_DECLINE: "Accept or decline [a/d]"}

    VALIDATOR = {ACCEPT_OR_DECLINE: lambda x: x in ["a", "A", "d", "D"]}

    def __init__(self, *args, **kwargs):
        super(Responder, self).__init__(*args, **kwargs)

    def check_pending(self):
        self.socket.sendall("u")
        self.socket.sendall(self.userid)

        offers = [models.Request(**request) for request in json.loads(self.socket.recv(config.POST_SIZE))]

        if not offers:  # List is empty
            print "You have no pending requests"
        else:
            for offer in offers:
                print "Request received from Match\n" \
                      "Description: %s \n" \
                      "Value: %s\n" % (offer.message, offer.amount)
                print
                response = self.get_input(Responder.ACCEPT_OR_DECLINE).lower()

                if response == "a":
                    print "Request accepted"
                    print "Request owner is %s (userid %s)" % (db.Database().user(offer.requester).name, offer.requester)
                else:
                    "print Request rejected"

                self.socket.sendall(response)

    @decorator.validate
    def get_input(self, kind):
        print Responder.INFO.get(kind) + ":"
        return raw_input("> ")

    def start(self):
        super(Responder, self).start()

        while True:
            print "Please use one of the following commands to:\n" \
                  "[u] Update\n" \
                  "[x] Exit\n"

            option = raw_input("> ")
            if option == "x":
                self.exit(); break
            elif option == "u":
                self.check_pending()
            elif option == "l":
                self.list_all()
            else:
                pass


if __name__ == "__main__":
    client = Responder()
    client.start()
