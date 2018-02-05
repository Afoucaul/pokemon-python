import tkinter as tk


class MapFrame(tk.Frame):
    def __init__(self, master, pixelSize=4):
        super().__init__(master)

        self.pixelSize = pixelSize

        self.canvas = tk.Canvas(self)

        self.canvas.pack()

    def _draw_grid(self):
        height, width = self.overworld.size
        canvasHeight = self.canvas["height"]
        canvasWidth = self.canvas["width"]

        for i in range(height):
            step = i * self.pixelSize * self.tileset.tileSize
            self.canvas.create_line(0, step, canvasWidth, step)

        for j in range(width):
            step = j * self.pixelSize * self.tileset.tileSize
            self.canvas.create_line(step, 0, step, canvasHeight)

    def draw(self):
        self._draw_grid()
        # self._draw_map()
