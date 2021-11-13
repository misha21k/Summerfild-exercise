import re
import tkinter


class MainWindow(tkinter.Frame):

    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.regex = tkinter.StringVar()
        self.text = tkinter.StringVar()
        self.ignore = tkinter.BooleanVar()
        self.dotall = tkinter.BooleanVar()
        for i in range(10):
            setattr(self, f'nameGroup{i}', tkinter.StringVar())
            exec(f"self.nameGroup{i}.set('Group {i}')")
            setattr(self, f'group{i}', tkinter.StringVar())
        self.message = tkinter.StringVar()

        regexLabel = tkinter.Label(self, text="Regex:", anchor=tkinter.W,
                                   underline=0, width=15)
        regexEntry = tkinter.Entry(self, textvariable=self.regex,
                                   justify=tkinter.LEFT, width=70)
        textLabel = tkinter.Label(self, text="Text:", anchor=tkinter.W,
                                  underline=0)
        textEntry = tkinter.Entry(self, textvariable=self.text,
                                  justify=tkinter.LEFT)
        ignoreCheck = tkinter.Checkbutton(self, text="Ignore case", underline=0,
                                          variable=self.ignore)
        dotallCheck = tkinter.Checkbutton(self, text="Dotall", underline=0,
                                          variable=self.dotall)
        for i in range(10):
            exec(
                f"name{i}Label = tkinter.Label(self, textvariable=self.nameGroup{i}, "
                f"anchor=tkinter.W)\n"
                f"group{i}Label = tkinter.Label(self, textvariable=self.group{i}, "
                f"anchor=tkinter.W, relief=tkinter.SUNKEN)\n"
            )
        messageLabel = tkinter.Label(self, textvariable=self.message,
                                     anchor=tkinter.W, relief=tkinter.SUNKEN,
                                     text='Unmatched')

        regexLabel.grid(row=0, column=0, padx=2, pady=2,
                        sticky=tkinter.W)
        regexEntry.grid(row=0, column=1, padx=2, pady=2,
                        columnspan=4, sticky=tkinter.EW)
        textLabel.grid(row=1, column=0, padx=2, pady=2,
                       sticky=tkinter.W)
        textEntry.grid(row=1, column=1, padx=2, pady=2,
                       columnspan=4, sticky=tkinter.EW)
        ignoreCheck.grid(row=2, column=2, padx=2, pady=2,
                         sticky=tkinter.W)
        dotallCheck.grid(row=2, column=4, padx=2, pady=2,
                         sticky=tkinter.W)
        for i in range(10):
            exec(
                f"name{i}Label.grid(row={i+3}, column=0, padx=2, pady=2,"
                f"sticky=tkinter.W)\n"
                f"group{i}Label.grid(row={i+3}, column=1, padx=2, pady=2,"
                f"columnspan=5, sticky=tkinter.EW)\n"
            )
        messageLabel.grid(row=13, column=0, padx=2, pady=2,
                          columnspan=5, sticky=tkinter.EW)

        regexEntry.focus_set()
        parent.bind("<Alt-r>", lambda *ignore: regexEntry.focus_set())
        parent.bind("<Alt-t>", lambda *ignore: textEntry.focus_set())
        parent.bind("<Alt-i>", self.ignoreChanged)
        parent.bind("<Alt-d>", self.datallChanged)
        regexEntry.bind("<Any-KeyRelease>", self.calculate)
        textEntry.bind("<Any-KeyRelease>", self.calculate)
        parent.bind("<Control-q>", self.quit)
        parent.bind("<Escape>", self.quit)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)
        self.columnconfigure(3, weight=3)
        self.columnconfigure(4, weight=3)


    def ignoreChanged(self, *ignore):
        self.ignore.set(not self.ignore.get())
        self.calculate()


    def datallChanged(self, *ignore):
        self.dotall.set(not self.dotall.get())
        self.calculate()


    def calculate(self, *ignore):
        for i in range(9):
            exec(f"self.nameGroup{i}.set('Group {i}')")
            exec(f"self.group{i}.set('')")
        regex = self.regex.get()
        text = self.text.get()
        ignore_case = self.ignore.get()
        dotall = self.dotall.get()
        flags='(?'
        if ignore_case:
            flags += 'i'
        if dotall:
            flags += 's'
        if len(flags) > 2:
            regex = flags + ')' + regex
        try:
            rx = re.compile(regex)
        except re.error as err:
            self.message.set(err)
            return
        match = rx.search(text)
        if match is None:
            self.message.set("Unmatched")
            return
        if match.lastindex and match.lastindex > 9:
            self.message.set("Too many groups")
            return
        self.group0.set(match.group())
        for i, group in enumerate(match.groups('')):
            exec(f"self.group{i+1}.set('{group}')")
        for name, i in rx.groupindex.items():
            exec(f"self.nameGroup{i}.set(\"Group {i} \'{name}\'\")")
        self.message.set("Matched")


    def quit(self, event=None):
        self.parent.destroy()


application = tkinter.Tk()
application.title("Regex")
application.resizable(True, False)
application.columnconfigure(0, weight=1)
window = MainWindow(application)
application.protocol("WM_DELETE_WINDOW", window.quit)
application.mainloop()