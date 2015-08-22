import threading
import json

lock = threading.Lock()


class ABCJSON(object):
    def to_json(self):
        raise NotImplementedError()


class Service(ABCJSON):
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

    @property
    def requester(self):
        return self._requester

    def to_json(self):
        return json.dumps({'requester': self.requester,
                           'message': self.message,
                           'amount': self.amount,
                           'deadline': self._deadline,
                           'cancellable': self._cancellable,
                           'responders': self._responders,
                           'serviceid': self._serviceid})


class User(ABCJSON):
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

    @property
    def userid(self):
        return self._userid

    def to_json(self):
        return json.dumps({'userid': self._userid,
                           'name': self._name,
                           'email': self._email,
                           'skills': self._skills})
