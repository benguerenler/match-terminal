
import socket

class Client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def exit(self):
        self.socket.shutdown(1)
        self.socket.close()

    def post(self):
        # Tell the server p
        self.socket.sendall("p")

    def start(self):
        self.socket.connect(("", 8888))
        data = self.socket.recv(1024)
        print data

        # Enter id
        id_user = raw_input()
        self.socket.sendall(id_user)

        # receive greeting
        print self.socket.recv(1024)

        while True:
            print "Please use one of the following commands to:\n" \
                  "[p] Post a new service\n" \
                  "[r] Read your pending requests\n" \
                  "[x] Exit"

            option = raw_input()
            if option == "x":
                self.exit()
                break


if __name__ == "__main__":
    client = Client()
    client.start()
