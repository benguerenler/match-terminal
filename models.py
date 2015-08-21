import threading

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