from abc import ABCMeta, abstractmethod


class ABCStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def select_match(self, *arg, **kwargs):
        raise NotImplementedError


class NextInLineStrategy(ABCStrategy):
    def select_match(self, db, request):
        selected = "1" if int(request.requester) + 1 > len(db.users) else str(int(request.requester) + 1)
        return db.users.get(selected)
