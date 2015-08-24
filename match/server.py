import socket
import sys
import threading
import json
import config
from db import Database
from models import Request
from match import Matcher, NextInLineStrategy


class Server(object):
    REQUEST_COUNTER = 0

    def __init__(self):
        self.db = Database()
        self._match = Matcher(NextInLineStrategy())

    def socket_dance(self, conn):
        try:
            conn.send("Connected to Match system. Please enter your id first")

            # Be polite Server!
            while True:
                id_user = conn.recv(config.USERID_SIZE)
                if self.db.user(id_user) is not None:
                    break
                else:
                    print "Please try again"

            # log userid
            print "User id %s logged in" % id_user

            reply = "Hi " + self.db.user(id_user).name
            self.db.user(id_user).conn = conn
            conn.sendall(reply)

            while (True):
                option = conn.recv(config.OPTION_SIZE)
                if option == "p":
                    self.post(conn)
                elif option == "l":
                    self.list_all(conn)
                elif option == "u":
                    self.list_pending(conn)
                else:
                    pass

        except socket.error as err:
            pass

    def post(self, conn):
        data = json.loads(conn.recv(config.POST_SIZE))
        request = Request(**data)
        self.db.requests.append(request)

        print "Request #%s: '%s', %s received from user %s" % (
            request.requestid, request.short_message, request.amount, request.requester)
        print "Searching for a match..."

        matched_user = self._match.select_match(request)
        print "Request #%s match to user %s" % (request.requestid, matched_user.userid)
        print "Request forwarded to user %s" % matched_user.userid

    def list_all(self, conn):
        conn.sendall(json.dumps([request.formatting() for request in self.db.requests]))
        print "Requesting requests"

    def list_pending(self, conn):
        # ask for the userid
        userid = conn.recv(config.USERID_SIZE)
        user = self.db.user(userid)

        print "User %s requested update" % userid

        conn.sendall(json.dumps([request.formatting() for request in user.pending]))

        # Assumption: Receive request in the same order
        for request in user.pending:
            response = conn.recv(config.OPTION_SIZE)  # a or d

            # Remove pending request from user
            user.pending.remove(request)

            print "Request %s send to user %s" % (request.requestid, userid)
            if response == "a":
                # Update service to be fulfilled and closed
                request.responders.append(user)
                print "User %s accepted request %s" % (userid, request.requestid)
            else:
                print "User %s rejected request %s" % (userid, request.requestid)

                # Contact another user
                print "Searching for a new match..."
                matched_user = self._match.select_match(request)

                print "Request #%s match to user %s" % (request.requestid, matched_user.userid)
                print "Request forwarded to user %s" % matched_user.userid

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind socket to localhost and port
        try:
            s.bind((config.HOST, config.PORT))
        except socket.error as msg:
            print 'Bind failer. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        print 'Socket bind complete'

        # listen on socket
        s.listen(10)
        print 'Socket listening'

        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=self.socket_dance, args=(conn,))
            t.start()


if __name__ == "__main__":
    server = Server()
    server.start()
