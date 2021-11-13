#!/usr/bin/env python3
# Copyright (c) 2008 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. It is provided for educational
# purposes and is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import sys
import unicodedata


def print_unicode_table(words):
    print("decimal   hex   chr  {0:^40}".format("name"))
    print("-------  -----  ---  {0:-<40}".format(""))

    code = ord(" ")
    end = sys.maxunicode

    while code < end:
        c = chr(code)
        name = unicodedata.name(c, "*** unknown ***")
        flag = True
        for word in words:
            if word not in name.lower():
                flag = False
                break
        if flag:
            print("{0:7}  {0:5X}  {0:^3c}  {1}".format(code, name.title()))
        code += 1


words = []
i = 1
if len(sys.argv) > 1:
    while i < len(sys.argv):
        if sys.argv[i] in ("-h", "--help"):
            print("usage: {0} [string1] [string2] ... [stringN]".format(sys.argv[0]))
            words = 0
            break
        else:
            words.append(sys.argv[i].lower())
            i += 1
if words != 0:
    print_unicode_table(words)
