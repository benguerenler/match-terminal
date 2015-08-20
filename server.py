import socket
import sys
import threading

HOST = ''
PORT = 8888

class User:
    def __init__(self, userid, name, email, skills, conn=None):
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
        self._conn = value

    @property
    def name(self):
        return self._name

class Database:
    def __init__(self):
        self._users = {"1": User("1", "Kiko Fernnadez", "kiko.fernandez@it.uu.se",
                            ["computer", "no-questions-asked", "sports", "beer"], None),
                       "2": User("2", "Albert", "", ["languages", "computer", "javascript"], None)}
        self._services = []

    def user(self, id):
        return self._users.get(id)

    @property
    def services(self):
        return self._services



class Server:
    def __init__(self):
        self.db = Database()

    def socket_dance(self, conn):
        try:
            conn.send("Connected to server. Please enter your id first")

            # Be polite Server!
            id_user = conn.recv(1024)

            reply = "Hi " + self.db.user(id_user).name
            conn.sendall(reply)

            while (True):
                option = conn.recv(1)


        except socket.error as err:
            pass

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
