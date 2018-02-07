import tkinter as tk

import app


class MapFrame(tk.Frame):
    def __init__(self, master, tileSize=64):
        super().__init__(master)
        self.tileSize = tileSize

        self.canvas = tk.Canvas(self)
        self.hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.vbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.hbar.config(command=self.canvas.xview)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(
            xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        self.canvas.bind("<Button-1>", self.on_click)

    def draw(self):
        if app.App.instance.tileset and app.App.instance.overworld:
            self._draw_grid()
            # self._draw_map()
            self._configure()

    def canvas_to_map_coordinates(self, xClick, yClick):
        return (xClick-2) // (self.tileSize+1), (yClick-2) // (self.tileSize+1)

    def on_click(self, event):
        x, y = event.x, event.y
        print(x, y)
        print(self.canvas_to_map_coordinates(x, y))

    def _draw_grid(self):
        height, width = app.App.instance.overworld.size
        canvasHeight = height * (self.tileSize + 1)
        canvasWidth = width * (self.tileSize + 1)

        for i in range(height + 1):
            step = 1 + i * (self.tileSize + 1)
            self.canvas.create_line(1, step, canvasWidth, step)

        for j in range(width + 1):
            step = 1 + j * (self.tileSize + 1)
            self.canvas.create_line(step, 1, step, canvasHeight)

    def _configure(self):
        height, width = app.App.instance.overworld.size
        self.canvas.config(width=1 + width * (self.tileSize + 1))
        self.canvas['scrollregion'] = self.canvas.bbox("all")
