class Const:
    """
    >>> const = Const()
    >>> const.PI = 3.14
    >>> const.PI
    3.14
    >>> const.PI = 68
    ValueError: cannot change a const attribute
    >>> del const.PI
    ValueError: cannot delete a const attribute
    """
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ValueError("cannot change a const attribute")
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise ValueError("cannot delete a const attribute")
        raise AttributeError("'{0}' object has not attribute '{1}'"
                             .format(self.__class__.__name__, name))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
