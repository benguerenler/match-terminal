import socket
import sys
import threading
import json

HOST = ''
PORT = 8888

lock = threading.Lock()

class Service(object):
    def __init__(self, serviceid="", message="", amount="", deadline="", cancellable="", requester="", responders=[]):
        self._requester = requester
        self._message = message
        self._amount = amount
        self._deadline = deadline
        self._cancellable = cancellable
        self._responders = responders
        self._serviceid = serviceid

class User(object):
    def __init__(self, userid=None, name="", email="", skills=[], conn=None):
        self._userid = userid
        self._name = name
        self._email = email
        self._skills = skills
        self._conn = conn

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, value):
        with lock:
            self._conn = value

    @property
    def name(self):
        return self._name

class Database(object):
    def __init__(self):
        self._users = {"1": User("1", "Kiko Fernandez", "kiko.fernandez@it.uu.se",
                            ["computer", "no-questions-asked", "sports", "beer"], None),
                       "2": User("2", "Albert", "", ["languages", "computer", "javascript"], None)}
        self._services = []

    @property
    def users(self):
        return self._users

    def user(self, id):
        return self._users.get(id)

    @property
    def services(self):
        return self._services



class Server(object):
    def __init__(self):
        self.db = Database()

    def socket_dance(self, conn):
        try:
            conn.send("Connected to server. Please enter your id first")

            # Be polite Server!
            while True:
                id_user = conn.recv(1024)
                if self.db.user(id_user):
                    break
                else:
                    print "Please try again"

            reply = "Hi " + self.db.user(id_user).name
            conn.sendall(reply)

            while (True):
                option = conn.recv(1)
                if option == "p": self.post(conn)
                elif (option == "r"): self.fetch_requests()
                else: pass

        except socket.error as err:
            pass

    def post(self, conn):
        userid = conn.recv(5)
        user = self.db.user(userid)
        user.conn = conn
        data = json.loads(conn.recv(1024))
        service = Service(**data)
        self.db.services.append(service)

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind socket to localhost and port
        try:
            s.bind((HOST, PORT))
        except socket.error as msg:
            print 'Bind failer. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        print 'Socket bind complete'

        # listen on socket
        s.listen(10)
        print 'Socket listening'

        while True:
            conn, addr = s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            t = threading.Thread(target=self.socket_dance, args=(conn,))
            t.start()


if __name__ == "__main__":
    server = Server()
    server.start()
