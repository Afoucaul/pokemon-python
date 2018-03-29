import tkinter as tk
import tkinter.filedialog as tkfiledialog

from core.tileset import Tileset


class NewTilesetWizard(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.pathsFrame = tk.Frame(self)
        self.imageLabel = tk.Label(self.pathsFrame, text="Tileset image:")
        self.sizeLabel = tk.Label(self.pathsFrame, text="Tile size (px):")
        self.pathLabel = tk.Label(self.pathsFrame, text="Path to save:")
        self.imageEntry = tk.Entry(self.pathsFrame)
        self.sizeEntry = tk.Entry(self.pathsFrame)
        self.pathEntry = tk.Entry(self.pathsFrame)
        self.imageButton = tk.Button(
            self.pathsFrame, text="...", command=self.on_image_button)
        self.pathButton = tk.Button(
            self.pathsFrame, text="...", command=self.on_path_button)

        self.imageLabel.grid(column=0, row=0)
        self.sizeLabel.grid(column=0, row=1)
        self.pathLabel.grid(column=0, row=2)
        self.imageEntry.grid(column=1, row=0)
        self.sizeEntry.grid(column=1, row=1)
        self.pathEntry.grid(column=1, row=2)
        self.imageButton.grid(column=2, row=0)
        self.pathButton.grid(column=2, row=2)

        self.validateButton = tk.Button(
            self, text="Create", command=self.on_validate_button)

        self.pathsFrame.pack()
        self.validateButton.pack()

    def on_image_button(self):
        path = tkfiledialog.askopenfilename(
            title="Loading image from...",
            filetypes=(
                ("image files", "*.png;*.bmp;*.jpg)"),
                ("all files", "*.*")))
        if path:
            self.imageEntry.delete(0, tk.END)
            self.imageEntry.insert(0, path)

    def on_path_button(self):
        path = tkfiledialog.asksaveasfilename(
            title="Saving tileset to...",
            filetypes=(
                ("tilesets file", "*.tileset"),
                ("all files", "*.*")))
        if path:
            self.pathEntry.delete(0, tk.END)
            self.pathEntry.insert(0, path)

    def on_validate_button(self):
        try:
            size = int(self.sizeEntry.get())
        except ValueError:
            return

        imagePath = self.imageEntry.get()
        tilesetPath = self.pathEntry.get()

        tileset = Tileset(imagePath, size)
        tileset.dump(tilesetPath)

        self.destroy()
