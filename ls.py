import optparse
import os
import datetime
import collections
import locale

locale.setlocale(locale.LC_ALL, '')


def read_line():
    """The function reads arguments of command line"""
    p = optparse.OptionParser(description='The paths are optional; if not given . is used.',
                              usage='%prog [options] [path1 [path2 [... pathN]]]')
    p.add_option('-H', '--hidden',
                 action='store_true',
                 dest='hidden',
                 help='show hidden files [default: off]')
    p.add_option('-m', '--modified',
                 action='store_true',
                 dest='modified',
                 help='show last modified date/time [default: off]')
    p.add_option('-o', '--order',
                 choices=['name', 'n', 'modified', 'm', 'size', 's'],
                 default='name',
                 dest='order',
                 help="order by ('name', 'n', 'modified', 'm', 'size', 's') [default: %default]",
                 type='choice')
    p.add_option('-r', '--recursive',
                 action='store_true',
                 dest='recursive',
                 help='recurse into subdirectories [default: off]')
    p.add_option('-s', '--sizes',
                 action='store_true',
                 dest='sizes',
                 help='show sizes [default: off]')
    p.disable_interspersed_args()
    return p.parse_args()


def get_files(direct, options):
    """Get list of files and directories"""
    File = collections.namedtuple('File', 'path date size')
    files = []
    dirs = []
    if options.recursive:
        for dirpath, dirnames, filenames in os.walk(direct):
            if options.hidden:
                filenames = [filename for filename in filenames if filename[0] != '.']
                dirnames[:] = [dirname for dirname in dirnames if dirname[0] != '.']
            dirpath += '' if dirpath.endswith('\\') else '\\'
            for filename in filenames:
                path = dirpath + filename
                date = options.modified and datetime.datetime.fromtimestamp(int(os.path.getmtime(path)))
                size = options.sizes and os.path.getsize(path)
                files.append(File(path, date, size))
    else:
        direct += '' if direct.endswith('\\') else '\\'
        for filename in os.listdir(direct):
            if options.hidden and filename[0] == '.':
                continue
            path = direct + filename
            date = options.modified and datetime.datetime.fromtimestamp(int(os.path.getmtime(path)))
            if os.path.isfile(path):
                size = options.sizes and os.path.getsize(path)
                files.append(File(path, date, size))
            if os.path.isdir(path):
                size = options.sizes
                dirs.append(File(path, date, size))
    dirs = order_items(dirs, options, theseAreFiles=False)
    files = order_items(files, options)
    return dirs, files


def order_items(items, options, theseAreFiles=True):
    """The function order elements by sign"""
    if options.order in {'modified', 'm'} and options.modified:
        items.sort(key=lambda x: x.date)
        return items
    if options.order in {'size', 's'} and options.sizes and theseAreFiles:
        items.sort(key=lambda x: x.size)
        return items
    items.sort(key=lambda x: (x.path.upper(), x.date, x.size))
    return items


def output(files, dirs, options):
    """Output files and directories"""
    for file in files:
        if file.date:
            print(file.date, end=' ')
        if file.size:
            print('{0:>15n}'.format(file.size), end=' ')
        print(file.path)
    for direct in dirs:
        if direct.date:
            print(direct.date, end=' ')
        if direct.size and len(files):
            print('{0:>15}'.format(' '), end=' ')
        print(direct.path)
    print('{nfiles} file{fs}'.format(nfiles=len(files),
                                     fs='s' if len(files) != 1 else '',
                                     ),
          end='')
    if not options.recursive:
        print(', {ndirs} director{ds}'.format(ndirs=len(dirs),
                                              ds='ies' if len(dirs) != 1 else 'y'
                                              ))


def main():
    options, args = read_line()
    for direct in args:
        try:
            print('For {}:'.format(direct))
            dirs, files = get_files(direct, options)
            output(files, dirs, options)
        except FileNotFoundError as err:
            print(err)


main()
