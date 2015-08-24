from db import Database


class Matcher(object):
    def __init__(self, strategy):
        self._db = Database()
        self._strategy = strategy

    def select_match(self, request):
        selected_user = self._strategy.select_match(self._db, request)
        selected_user.pending.append(request)  # append item to list, non-atomic op
        return selected_user
