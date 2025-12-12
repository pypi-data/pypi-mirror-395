class Clay:

    def __init__(self, instance=None, **kwargs):
        d = self.__dict__
        if instance:
            d.update(instance.__dict__)
        d.update(kwargs)


class Mold:

    def __init__(self, defaults=None):
        self.defaults = defaults or {}

    def set(self, k, d, f=None):
        v = d.get(k)
        if v is None:
            x = self.defaults[k]
            v = x() if callable(x) else x
        if f:
            v = f(v)
        setattr(self, k, v)
