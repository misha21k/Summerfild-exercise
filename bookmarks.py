import shelve
from pickle import HIGHEST_PROTOCOL
import os.path
import Util
import Console
import sys


def main():
    functions = dict(a=add_bookmark, e=edit_bookmark, l=list_bookmarks,
                     r=remove_bookmarks, q=quit)
    filename = os.path.join(os.path.dirname(__file__), "bookmarks.dbm")
    db = None
    try:
        db = shelve.open(filename, protocol=HIGHEST_PROTOCOL)
        print(f'Bookmarks ({os.path.basename(filename)})')
        action = ""
        while True:
            if action != 'l' and len(db):
                list_bookmarks(db)
            else:
                print("{0} bookmark{1}".format(len(db), Util.s(len(db))))
            print()
            menu = ('(A)dd (E)dit (L)ist (R)emove (Q)uit'
                    if len(db) else '(A)dd (Q)uit')
            valid = 'aelrq' if len(db) else 'aq'
            action = Console.get_menu_choice(menu, valid, 'l' if len(db) else 'a', True)
            functions[action](db)
    finally:
        if db is not None:
            db.close()


def add_bookmark(db):
    name = Console.get_string('Name', 'name')
    if not name:
        return
    url = Console.get_string('URL', 'url')
    if not url:
        return
    if not url.startswith('http://'):
        url = 'http://' + url
    db[name] = url
    db.sync()



def edit_bookmark(db):
    old_name = find_bookmark(db, 'edit')
    if old_name is None:
        return
    url = db[old_name]
    name = Console.get_string('Name', 'name', old_name)
    if not name:
        return
    url = Console.get_string('URL', 'url', url)
    if not url:
        return
    if not url.startswith('http://'):
        url = 'http://' + url
    if name != old_name:
        del db[old_name]
    db[name] = url
    db.sync()



def list_bookmarks(db):
    digits = len(str(len(db)))
    for i, name in enumerate(sorted(db.keys(), key=str.lower)):
        url = db[name]
        print(f"({i + 1:>{digits}}) {name:.<31} {url}")


def remove_bookmarks(db):
    name = find_bookmark(db, 'edit')
    answer = Console.get_bool(f'Do you want to delete bookbark {name}?')
    if answer:
        del db[name]
        db.sync()


def find_bookmark(db, action):
    number = Console.get_integer(f'Number of bookmark to {action}', 'number',
                                 minimum=1, maximum=len(db))
    if number == 0:
        return None
    names = sorted(db.keys(), key=str.lower)
    return names[number - 1]


def quit(db):
    print("Saved {0} bookmark{1}".format(len(db), Util.s(len(db))))
    db.close()
    sys.exit()

main()
