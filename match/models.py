import threading

lock = threading.Lock()

class ABCJSON(object):

    def formatting(self):
        return {key[1:]: value for key, value in self.__dict__.iteritems()}


class Service(ABCJSON):
    def __init__(self, serviceid="", message="", amount="", deadline="", cancellable="",
                       requester="", responders=[], waiting_list=[]):
        self._requester = requester
        self._message = message
        self._amount = amount
        self._deadline = deadline
        self._cancellable = cancellable
        self._responders = responders
        self._serviceid = serviceid
        self._waiting_list = waiting_list

    @property
    def serviceid(self):
        return self._serviceid

    @property
    def message(self):
        return self._message

    @property
    def short_message(self):
        return self._message[:100] + "..."

    @property
    def requester(self):
        return self._requester

    @property
    def amount(self):
        return self._amount

    @property
    def deadline(self):
        return self._deadline

    @property
    def waiting_list(self):
        return self._waiting_list

    @property
    def responders(self):
        return self._responders

    @responders.setter
    def responders(self, responders):
        self._responders = responders

    def formatting(self):
        return super(Service, self).formatting()


class User(ABCJSON):
    def __init__(self, userid=None, name="", email="", skills=[], conn=None, pending=[]):
        self._userid = userid
        self._name = name
        self._email = email
        self._skills = skills
        self._pending = pending
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

    @property
    def userid(self):
        return self._userid

    @property
    def pending(self):
        return self._pending

    @pending.setter
    def pending(self, services):
        self._pending = services

    def formatting(self):
        return super(User, self).formatting()
