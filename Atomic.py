"""
>>> items = [1, 'hello', 3]
>>> with Atomic(items) as atomic:
...     atomic.append(5)
...     del atomic[1]
...     atomic[1] = 'hi'
>>> items
[1, 'hi', 5]
>>> items = 'Hello'
>>> try:
...     with Atomic(items) as atomic:
...         pass
... except AssertionError as err:
...     print("no changes applied:", err)
no changes applied: wrong type of collection
>>> items
'Hello'
>>> items = {1, 2, 3}
>>> with Atomic(items) as atomic:
...     atomic.add(4)
...     atomic -= {2, 3}
>>> items
{1, 4}
>>> items = dict(a=5, b=8, c=12)
>>> with Atomic(items) as atomic:
...     atomic['d'] = 34
...     del atomic['b']
>>> items
{'a': 5, 'c': 12, 'd': 34}
>>> items = [1, 2, [3, 4]]
>>> try:
...     with Atomic(items) as atomic:
...         atomic[2].append(5)
...         print(atomic[3])  # IndexError
... except IndexError:
...    pass
>>> items
[1, 2, [3, 4, 5]]
>>> try:
...     with Atomic(items, shallow_copy=False) as atomic:
...         atomic[2].append(6)
...         print(atomic[3])  # IndexError
... except IndexError:
...     pass
>>> items
[1, 2, [3, 4, 5]]
>>> items = dict(a=5, b=[1, 2])
>>> try:
...     with Atomic(items) as atomic:
...         atomic['b'].append(3)
...         raise AssertionError
... except AssertionError:
...     pass
>>> items
{'a': 5, 'b': [1, 2, 3]}
>>> try:
...     with Atomic(items, shallow_copy=False) as atomic:
...         atomic['b'].append(4)
...         raise AssertionError
... except AssertionError:
...     pass
>>> items
{'a': 5, 'b': [1, 2, 3]}
"""


import copy
import collections.abc as abc
import doctest


class Atomic:

    def __init__(self, collection, shallow_copy=True):
        self.original = collection
        if isinstance(collection, (abc.MutableMapping, abc.MutableSet)):
            self.change = self.change_set
        elif isinstance(collection, abc.MutableSequence):
            self.change = self.change_list
        else:
            raise AssertionError('wrong type of collection')
        self.copy = copy.copy if shallow_copy else copy.deepcopy

    def change_set(self, original, modified):
        original.clear()
        original.update(modified)

    def change_list(self, original, modified):
        original[:] = modified


    def __enter__(self):
        self.modified = self.copy(self.original)
        return self.modified

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.change(self.original, self.modified)


if __name__ == '__main__':
    doctest.testmod()
