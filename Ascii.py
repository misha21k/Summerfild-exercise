import string
import doctest

is_ascii = lambda s: all(map(lambda x: ord(x) < 127, s))
is_ascii.__doc__ = """\
    >>> is_ascii('Hello word!')
    True
    >>> is_ascii('Привет мир!')
    False
    """

is_ascii_punctuation = lambda s: all(map(lambda x: x in string.punctuation, s))
is_ascii_punctuation.__doc__ = """\
    >>> is_ascii_punctuation('(!.')
    True
    """

is_ascii_printable = lambda s: all(map(lambda x: x in string.printable, s))
is_ascii_printable.__doc__ = """\
    >>> is_ascii_printable('\b')
    False
    """

if __name__ == '__main__':
    doctest.testmod()
