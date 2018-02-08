import tkinter as tk
from collections import OrderedDict


class RadiobuttonPanel(tk.Frame):
    def __init__(self, master, *options, orient=tk.HORIZONTAL):
        super().__init__(master)

        self.options = options
        self.variable = tk.StringVar()
        self.radiobuttons = []

        for option in self.options:
            self.radiobuttons.append(
                tk.Radiobutton(
                    self, text=option, variable=self.variable, value=option))
        self.variable.set(options[0])

        side = tk.TOP if orient == tk.VERTICAL else tk.LEFT
        for rb in self.radiobuttons:
            rb.pack(side=side, anchor="w")

    def trace(self, callback):
        self.variable.trace('w', callback)

    def set(self, value):
        self.variable.set(value)

    def get(self):
        return self.variable.get()

    def reset(self):
        self.set(self.options[0])


class EnumPanel(tk.Frame):
    def __init__(self, master, enum, orient=tk.HORIZONTAL):
        super().__init__(master)

        self.enum = enum
        self.variable = tk.Variable()
        self.checkbuttons = OrderedDict()

        for k, v in self.enum.__members__.items():
            var = tk.IntVar()
            self.checkbuttons[v] = (
                var, tk.Checkbutton(self, text=k.title(), variable=var))
            var.trace('w', self.on_option_selected)

        side = tk.TOP if orient == tk.VERTICAL else tk.LEFT
        for cb in self.checkbuttons.values():
            cb[1].pack(side=side, anchor="w")

    def on_option_selected(self, *_):
        self.variable.set(True)

    def trace(self, callback):
        self.variable.trace('w', callback)

    def get(self):
        return [k for k, v in self.checkbuttons.items() if v[0].get()]
