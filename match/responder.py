from abcclient import ABCClient


class Responder(ABCClient):

    def __init__(self, *args, **kwargs):
        super(Responder, self).__init__(*args, **kwargs)

    def pending(self):
        self.socket.sendall("r")
        self.socket.sendall(self.userid)

    def list_all(self):
        pass

    def start(self):
        super(Responder, self).start()

        while True:
            print "Please use one of the following commands to:\n" \
                  "[r] Read your pending requests\n" \
                  "[l] list all\n" \
                  "[x] Exit\n"

            option = raw_input("> ")
            if option == "x": self.exit(); break
            elif option == "r": self.pending()
            elif option == "l": self.list_all()
            else: pass


if __name__ == "__main__":
    client = Responder()
    client.start()
