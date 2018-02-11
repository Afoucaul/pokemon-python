import tkinter as tk
import tkinter.filedialog as tkfiledialog

from wizards.new_tileset import NewTilesetWizard

import app


class MainMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        self.mapMenu = tk.Menu(self, tearoff=False)
        self.mapMenu.add_command(
            label="Load...", command=self.map_load_command)
        self.mapMenu.add_command(
            label="Save", command=self.map_save_command)
        self.mapMenu.add_command(
            label="Save as...", command=self.map_save_as_command)
        self.mapMenu.add_command(
            label="Close", command=self.map_close_command)

        self.tilesetMenu = tk.Menu(self, tearoff=False)
        self.tilesetMenu.add_command(
            label="New...", command=self.tileset_new_command)
        self.tilesetMenu.add_command(
            label="Load...", command=self.tileset_load_command)

        self.add_cascade(label="Map", menu=self.mapMenu)
        self.add_cascade(label="Tileset", menu=self.tilesetMenu)

    def map_load_command(self):
        path = tkfiledialog.askopenfilename(
            title="Loading map from...",
            filetypes=(("map files", "*.map"), ("all files", "*.*")))
        if path:
            app.App.instance.load_overworld(path)

    def map_save_command(self):
        print("Saving map...")
        app.App.instance.save_overworld()

    def map_save_as_command(self):
        print("Saving map as...")
        path = tkfiledialog.asksaveasfilename(
            title="Saving map to...",
            filetypes=(("map files", "*.map"), ("all files", "*.*")))
        if path:
            app.App.instance.save_overworld(path)

    def map_close_command(self):
        print("Closing map...")
        app.App.instance.close_overworld()

    def tileset_load_command(self):
        print("Loading tileset...")
        path = tkfiledialog.askopenfilename(
            title="Loading tileset from...",
            filetypes=(("tileset files", "*.tileset"), ("all files", "*.*")))
        if path:
            app.App.instance.load_tileset(path)

    def tileset_new_command(self):
        NewTilesetWizard(self.master)
