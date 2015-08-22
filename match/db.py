from models import User

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
