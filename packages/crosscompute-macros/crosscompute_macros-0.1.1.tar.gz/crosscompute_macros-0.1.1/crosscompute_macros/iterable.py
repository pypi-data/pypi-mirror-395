import operator
from collections import OrderedDict, defaultdict


class LRUDict(OrderedDict):
    # https://gist.github.com/davesteele/44793cd0348f59f8fadd49d7799bd306

    def __init__(self, *args, length: int, **kwargs):
        if length <= 0:
            raise ValueError
        self._length = length
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        super().move_to_end(key)
        while len(self) > self._length:
            super().__delitem__(next(iter(self)))

    def __getitem__(self, key):
        value = super().__getitem__(key)
        super().move_to_end(key)
        return value


class InfiniteDefaultDict(dict):

    def __getitem__(self, key):
        if key in self:
            value = super().__getitem__(key)
        else:
            value = InfiniteDefaultDict()
            super().__setitem__(key, value)
        return value


def apply_functions(value, function_names, function_by_name):
    for function_name in function_names:
        function_name = function_name.strip()
        if not function_name:
            continue
        f = function_by_name[function_name]
        value = f(value)
    return value


def get_unique_order(texts):
    return list(dict.fromkeys([_.strip() for _ in texts]))


def group_by_attribute(items, name):
    d = defaultdict(list)
    for item in items:
        d[getattr(item, name)].append(item)
    return dict(d)


def find_item(
        items, key, value, get_value=lambda item, key: getattr(item, key),
        normalize=lambda _: _, compare=operator.eq):
    normalized_value = normalize(value)

    def is_match(item):
        try:
            v = get_value(item, key)
        except KeyError:
            is_match = False
        else:
            normalized_v = normalize(v)
            is_match = compare(normalized_value, normalized_v)
        return is_match

    return next(filter(is_match, items))


def drop_null_values(d):
    keys = list(d.keys())
    for k in keys:
        if d[k] is None:
            del d[k]
    return d
