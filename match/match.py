from db import Database
from abc import ABCMeta, abstractmethod


class ABCStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def select_match(self, *arg, **kwargs):
        raise NotImplementedError


class NextInLineStrategy(ABCStrategy):

    def select_match(self, db, request):
        selected =  "1" if int(request.requester) + 1 > len(db.users) else str(int(request.requester) + 1)
        return db.users.get(selected)


class Matcher(object):
    def __init__(self, strategy):
        self._db = Database()
        self._strategy = strategy

    def select_match(self, request):
        selected_user =  self._strategy.select_match(self._db, request)
        selected_user.pending.append(request)  # append item to list, non-atomic op
        return selected_user
