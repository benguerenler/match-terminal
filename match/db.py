from models import User
import threading

# Define them as global => shared between multiple instances of Database
_users = {"1": User("1", "Kiko Fernandez", "kiko.fernandez@it.uu.se",
                    ["computer", "no-questions-asked", "sports", "beer"], None),
          "2": User("2", "Albert", "", ["languages", "computer", "javascript"], None)}
_requests = []


lock = threading.Lock()
REQUEST_COUNTER = 0

def inc_request_counter():
    with lock:
        global REQUEST_COUNTER
        REQUEST_COUNTER += 1
        return REQUEST_COUNTER

class Database(object):
    def __init__(self):
        self._users = _users
        self._requests = _requests

    @property
    def users(self):
        return self._users

    def user(self, id):
        return self._users.get(id)

    @property
    def requests(self):
        return self._requests
