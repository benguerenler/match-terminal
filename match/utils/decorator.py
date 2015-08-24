__author__ = 'kikofernandezreyes'

def validate(func):
    def _decorator(this, kind):
        data = func(this, kind)
        validator = this.VALIDATOR.get(kind)
        if validator(data):
            return data
        else:
            return _decorator(this, kind)

    return _decorator