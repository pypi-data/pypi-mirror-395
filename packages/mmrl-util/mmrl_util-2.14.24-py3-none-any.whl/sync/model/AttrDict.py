from functools import reduce

class AttrDict(dict):
    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getattr__(self, item):
        return self.get(item)

    def __hash__(self):
        return hash(frozenset(self.__dict__.items()))

    def deep_get(self, keys, default=None):
        return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), self)

    def copy(self, **kwargs):
        new = super().copy()
        new.update(**kwargs)

        return AttrDict(new)
