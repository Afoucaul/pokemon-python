import tkinter as tk
from PIL import ImageTk

import app


class TilesetFrame(tk.Frame):
    select_style = {'width': 5, 'outline': "blue"}
    hover_style = {'fill': "blue", 'stipple': "gray25", 'width': 0}

    def __init__(self, master, tileSize=64, tilesPerRow=4):
        super().__init__(master)
        self.tileSize = tileSize
        self.tilesPerRow = tilesPerRow

        self.canvas = tk.Canvas(self)
        self.canvas.hovered_tile = None
        self.canvas.hover_rectangle = None
        self.canvas.selected_tile = None
        self.canvas.select_rectangle = None
        self.canvas.tiles = None
        self.vbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.Y)

        self.vbar['command'] = self.canvas.yview
        self.canvas['yscrollcommand'] = self.vbar.set

        self.canvas.bind("<Button-1>", self.on_click_canvas)
        self.canvas.bind("<Motion>", self.on_motion_canvas)
        self.canvas.bind("<Leave>", self.on_leave_canvas)

    def selected_tile(self):
        if self.canvas.selected_tile is not None:
            return self.canvas.tiles[self.canvas.selected_tile][0]

    def _configure(self):
        self.canvas.config(
            width=1 + (1+self.tileSize) * self.tilesPerRow)
        self.canvas['scrollregion'] = self.canvas.bbox("all")

    def _draw_grid(self):
        *_, canvasWidth, canvasHeight = self.canvas.bbox("all")

        for i in range((canvasHeight // (self.tileSize+1)) + 1):
            step = 1 + i * (self.tileSize + 1)
            self.canvas.create_line(1, step, canvasWidth, step)

        for j in range(self.tilesPerRow + 1):
            step = 1 + j * (self.tileSize + 1)
            self.canvas.create_line(step, 1, step, canvasHeight)

    def _draw_tiles(self):
        tileset = app.App.instance.tileset
        self.canvas.tiles = {}

        for i in range(tileset.rowCount):
            for j in range(tileset.columnCount):
                index = i*tileset.columnCount + j
                tile = ImageTk.PhotoImage(
                    tileset.get_tile(index, self.tileSize))
                tileId = self.canvas.create_image(
                    2 + (index % self.tilesPerRow) * (self.tileSize + 1),
                    2 + (index // self.tilesPerRow) * (self.tileSize + 1),
                    image=tile,
                    anchor="nw")
                self.canvas.tiles[tileId] = (index, tile)

    def draw(self):
        if app.App.instance.tileset:
            self._draw_tiles()
            self._draw_grid()
            self._configure()

    def on_click_canvas(self, event):
        if self.canvas.hovered_tile != self.canvas.selected_tile:
            self.canvas.delete(self.canvas.select_rectangle)
            self.canvas.selected_tile = self.canvas.hovered_tile
            rectangle = self.canvas.bbox(tk.CURRENT)
            self.canvas.select_rectangle = self.canvas.create_rectangle(
                *rectangle, **self.select_style)

    def on_motion_canvas(self, event):
        if self.canvas.select_rectangle in self.canvas.find_withtag(tk.CURRENT):
            self.canvas.delete(self.canvas.hover_rectangle)
            self.canvas.hovered_tile = self.canvas.selected_tile
            self.canvas.hover_rectangle = None

        tileId = [cid for cid in self.canvas.find_withtag(tk.CURRENT)
                  if cid in self.canvas.tiles]

        if tileId:
            tileId = tileId[0]
            if tileId != self.canvas.hovered_tile:
                self.canvas.delete(self.canvas.hover_rectangle)
                self.canvas.hovered_tile = tileId
                rectangle = self.canvas.bbox(tk.CURRENT)
                self.canvas.hover_rectangle = self.canvas.create_rectangle(
                    *rectangle, **self.hover_style)

    def on_leave_canvas(self, event):
        self.canvas.delete(self.canvas.hover_rectangle)
        self.canvas.hover_rectangle = None
        self.canvas.hovered_tile = None

    def get_tile(self, index):
        for tileId, tile in self.canvas.tiles.values():
            if tileId == index:
                return tile
