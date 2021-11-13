
"""
>>> import shutil
>>> import sys
>>> import tempfile

>>> S = struct.Struct("<15s")
>>> fileA = os.path.join(tempfile.gettempdir(), "fileA.dat")
>>> fileB = os.path.join(tempfile.gettempdir(), "fileB.dat")
>>> for name in (fileA, fileB):
...     try:
...         os.remove(name)
...     except EnvironmentError:
...         pass

>>> brf = BinaryRecordFile(fileA, S.size)
>>> for i, text in enumerate(("Alpha", "Bravo", "Charlie", "Delta",
...        "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet",
...        "Kilo", "Lima", "Mike", "November", "Oscar", "Papa",
...        "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor",
...        "Whisky", "X-Ray", "Yankee", "Zulu")):
...     brf.append(S.pack(text.encode("utf8")))
>>> assert len(brf) == 26
>>> shutil.copy(fileA, fileB)
>>> del brf[12]
>>> assert len(brf) == 25
>>> brf.close()

>>> if ((os.path.getsize(fileA) + S.size) !=
...        os.path.getsize(fileB)):
...     print("FAIL#1: expected file sizes are wrong")
...     sys.exit()

>>> shutil.copy(fileB, fileA)
>>> if os.path.getsize(fileA) != os.path.getsize(fileB):
...     print("FAIL#2: expected file sizes differ")
...     sys.exit()

>>> for name in (fileA, fileB):
...     try:
...         os.remove(name)
...     except EnvironmentError:
...         pass

>>> filename =  os.path.join(tempfile.gettempdir(), "test.dat")
>>> if os.path.exists(filename): os.remove(filename)
>>> S = struct.Struct("<8s")
>>> test = BinaryRecordFile(filename, S.size)
>>> test.append(S.pack(b"Alpha"))
>>> test.append(S.pack(b"Bravo"))
>>> test.append(S.pack(b"Charlie"))
>>> test.append(S.pack(b"Delta"))
>>> test.append(S.pack(b"Echo"))
>>> test.close()
>>> os.path.getsize(filename)
40
>>> test = BinaryRecordFile(filename, S.size)
>>> len(test)
5
>>> for index in range(len(test)):
...     del test[0]
>>> test.close()
>>> os.path.getsize(filename)
0
>>> test = BinaryRecordFile(filename, S.size)
>>> test.append(S.pack(b"Alpha"))
>>> test.append(S.pack(b"Bravo"))
>>> test.append(S.pack(b"Charlie"))
>>> test.append(S.pack(b"Delta"))
>>> test.append(S.pack(b"Echo"))
>>> del test[2]
>>> del test[3]
>>> del test[2]
>>> test.close()
>>> os.path.getsize(filename)
16
>>> test = BinaryRecordFile(filename, S.size)
>>> test[0] = S.pack(b"Alpha")
>>> test[1] = S.pack(b"Bravo")
>>> test.append(S.pack(b"Charlie"))
>>> test.append(S.pack(b"Delta"))
>>> test.append(S.pack(b"Echo"))
>>> S.unpack(test[2])[0].startswith(b"Charlie")
True
>>> test.close()
>>> os.path.getsize(filename)
40
>>> os.remove(filename)
"""

import os
import struct


class BinaryRecordFile:

    def __init__(self, filename, record_size, auto_flush=True):
        """A random access binary file that behaves rather like a list
        with each item a bytes or bytesarray object of record_size.
        """
        self.__record_size = record_size
        mode = "w+b" if not os.path.exists(filename) else "r+b"
        self.__fh = open(filename, mode)
        self.auto_flush = auto_flush


    @property
    def record_size(self):
        "The size of each item"
        return self.__record_size


    @property
    def name(self):
        "The name of the file"
        return self.__fh.name


    def flush(self):
        """Flush writes to disk
        Done automatically if auto_flush is True
        """
        self.__fh.flush()


    def close(self):
        self.__fh.close()


    def append(self, record):
        """Appends new record in end"""
        assert isinstance(record, (bytes, bytearray)), \
            "binary data required"
        assert len(record) == self.record_size, (
            "record must be exactly {0} bytes".format(
            self.record_size))
        self.__fh.seek(0, os.SEEK_END)
        self.__fh.write(record)
        if self.auto_flush:
            self.__fh.flush()


    def __setitem__(self, index, record):
        """Sets the item at position index to be the given record

        The index position can be beyond the current end of the file.
        """
        assert isinstance(record, (bytes, bytearray)), \
               "binary data required"
        assert len(record) == self.record_size, (
            "record must be exactly {0} bytes".format(
            self.record_size))
        self.__seek_to_index(index)
        self.__fh.write(record)
        if self.auto_flush:
            self.__fh.flush()


    def __getitem__(self, index):
        """Returns the item at the given index position

        If there is no item at the given position, raises an
        IndexError exception.
        """
        self.__seek_to_index(index)
        return self.__fh.read(self.record_size)
        

    def __seek_to_index(self, index):
        if self.auto_flush:
            self.__fh.flush()
        self.__fh.seek(0, os.SEEK_END)
        end = self.__fh.tell()
        offset = index * self.__record_size
        if offset >= end:
            raise IndexError("no record at index position {0}".format(
                             index))
        self.__fh.seek(offset)


    def __delitem__(self, index):
        """Deletes the item at the given index position."""
        self.__seek_to_index(index)
        offset = (index + 1) * self.__record_size
        self.__fh.seek(offset)
        next_items = self.__fh.read()
        offset = index * self.__record_size
        self.__fh.seek(offset)
        self.__fh.write(next_items)
        self.__fh.truncate()
        self.__fh.flush()


    def __len__(self):
        """The number number of record positions.

        This is the maximum number of records there could be at
        present. The true number may be less because some records
        might be deleted.
        """
        if self.auto_flush:
            self.__fh.flush()
        self.__fh.seek(0, os.SEEK_END)
        end = self.__fh.tell()
        return end // self.__record_size


if __name__ == "__main__":
    import doctest
    doctest.testmod()
