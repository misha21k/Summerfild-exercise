import os


class NewFile(Exception): pass
class ExitProgram(Exception): pass

save = False

def main():
    global save

    files = [file for file in os.listdir(".") if file.endswith(".lst")]
    try:
        if files:
            list_output(files)
        else:
            print("-- no files in the list --")
            raise NewFile
        num_file = get_integer("Enter the file number(or 0 to add file)",
                               "file number", default=0, minimum=0,
                               maximum=len(files))
        if num_file == 0:
            raise NewFile
    except NewFile:
        new_file(files)
        num_file = -1

    filename = files[num_file-1]
    items = read_file(filename)
    try:
        while True:
            if items:
                list_output(items)
                choice_of_action(filename, items, save=save)
            else:
                choice_of_action(filename, items, delete=False, save=save)
    except ExitProgram:
        pass


def new_file(files):
    while True:
        try:
            files.append(get_string("Enter name of new file", "file name",
                                    minimum_length=1))
            if not files[-1].endswith(".lst"):
                files[-1] += ".lst"
            file = open(files[-1], "w")
            file.close()
            break
        except OSError:
            input("Enter correct file name")


def list_output(items):
    num_format = len(str(len(items)))
    sorted_items = sorted(items, key=str.lower)
    print("")
    for num, item in enumerate(sorted_items, 1):
        print("{0:>{1}}: {2}".format(num, num_format, item))


def read_file(filename):
    print("Choose filename: {}".format(filename))
    file = open(filename, encoding="utf-8")
    items = [line.rstrip("\n") for line in file]
    file.close()
    if not items:
        print("\n-- no items are in list --")
    return items


def choice_of_action(filename, items, delete=True, save=True):
    choice = input("[A]dd {0}{1}[Q]uit [a]: ".format("[D]elate " * delete,
                                                     "[S]ave" * save)).lower()
    if choice == "a":
        add_item(items)
    elif choice == "d" and delete:
        delete_item(items)
    elif choice == "s" and save:
        save_items(filename, items)
    elif choice == "q":
        quit_code(filename, items)
    else:
        input("ERROR: invalid choice--enter one of 'Aa{0}{1}Qq'\n"
              "Press Enter to continue...".format("Dd" * delete, "Ss" * save))


def add_item(items):
    new_item = get_string("Add item")
    if new_item:
        items.append(new_item)
        global save
        save = True


def delete_item(items):
    num = get_integer("Delete item number(or 0 to cancel)", "item number",
                maximum=len(items))
    if num:
        sorted_items = sorted(items, key=str.lower)
        items.remove(sorted_items[num-1])
        global save
        save = True


def save_items(filename, items):
    global save
    file = open(filename, "w")
    for line in items:
        file.write(line+"\n")
    file.close()
    n = len(items)
    print("Saved {0} item{1} to {2}".format(n, "" if n == 1 else "s", filename))
    save = False


def quit_code(filename, items):
    global save
    if save:
        while True:
            yes_no = get_string("Save unsaved changes (y/n)", default="y")
            if yes_no in {"y", "yes"}:
                save_items(filename, items)
                break
            elif yes_no in {"n", "no"}:
                break
            else:
                print("Enter 'n', 'no' or 'y', 'yes'")
    raise ExitProgram


def get_string(message, name="string", default=None,
               minimum_length=0, maximum_length=80):
    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line:
                if default is not None:
                    return default
                if minimum_length == 0:
                    return ""
                else:
                    raise ValueError("{0} may not be empty".format(
                                     name))
            if not (minimum_length <= len(line) <= maximum_length):
                raise ValueError("{0} must have at least {1} and" 
                        "at most {2} characters".format(
                        name, minimum_length, maximum_length))
            return line
        except ValueError as err:
            print("ERROR", err)


def get_integer(message, name="integer", default=None, minimum=0,
                maximum=100, allow_zero=True):

    class RangeError(Exception): pass

    message += ": " if default is None else " [{0}]: ".format(default)
    while True:
        try:
            line = input(message)
            if not line and default is not None:
                return default
            i = int(line)
            if i == 0:
                if allow_zero:
                    return i
                else:
                    raise RangeError("{0} may not be 0".format(name))
            if not (minimum <= i <= maximum):
                raise RangeError("{0} must be between {1} and {2} "
                        "inclusive{3}".format(name, minimum, maximum,
                        (" (or 0)" if allow_zero else "")))
            return i
        except RangeError as err:
            print("ERROR", err)
        except ValueError:
            print("ERROR {0} must be an integer".format(name))


main()