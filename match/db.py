from models import User
import threading

# Define them as global => shared between multiple instances of Database
_users = {"1": User("1", "Kiko Fernandez", "kiko.fernandez@it.uu.se",
                    ["computer", "no-questions-asked", "sports", "beer"], None),
          "2": User("2", "Albert", "", ["languages", "computer", "javascript"], None)}
_services = []


lock = threading.Lock()
SERVICE_COUNTER = 0

def inc_service_counter():
    with lock:
        global SERVICE_COUNTER
        SERVICE_COUNTER += 1
        return SERVICE_COUNTER

class Database(object):
    def __init__(self):
        self._users = _users
        self._services = _services

    @property
    def users(self):
        return self._users

    def user(self, id):
        return self._users.get(id)

    @property
    def services(self):
        return self._services
