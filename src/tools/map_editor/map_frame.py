import tkinter as tk
import numpy as np
from collections import OrderedDict

import app
from utils import RadiobuttonPanel


class MapFrame(tk.Frame):
    labelToLayer = OrderedDict()
    labelToLayer['Lower graphical layer'] = "lowerTiles"
    labelToLayer['Upper graphical layer'] = "upperTiles"
    labelToLayer['Collision layer'] = "collisions"

    hover_style = {'fill': "red", 'stipple': "gray25", 'width': 0}

    def __init__(self, master, tileSize=32):
        super().__init__(master)
        self.tileSize = tileSize
        self.currentLayer = None
        self.graphicalLayers = {v: None for v in self.labelToLayer.values()}
        self.currentGraphicalLayer = None
        self.clicked = False
        self.tiles = []

        self.canvas = tk.Canvas(self)
        self.canvas.hovered_cell = None
        self.canvas.hover_rectangle = None
        self.hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.vbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.radiobuttons = RadiobuttonPanel(self, *self.labelToLayer.keys())

        self.radiobuttons.pack()
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.hbar.config(command=self.canvas.xview)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(
            xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

    def do_bindings(self):
        self.canvas.bind("<Motion>", self.on_motion_canvas)
        self.canvas.bind("<Leave>", self.on_leave_canvas)
        self.canvas.bind("<ButtonPress-1>", self.on_click_down_canvas)
        self.canvas.bind("<ButtonRelease-1>", self.on_click_up_canvas)
        self.radiobuttons.trace(self.on_layer_selected)

    def undo_bindings(self):
        self.canvas.unbind("<Motion>")
        self.canvas.unbind("<Leave>")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<ButtonRelease-1>")

    def clear(self):
        self.clear_graphical_layers()
        self.currentLayer = None

    def draw(self):
        if app.App.instance.tileset and app.App.instance.overworld:
            self._draw_grid()
            self._draw_map()
            self._configure()

    def on_tileset_load(self):
        self.tiles = app.App.instance.tileset.get_tiles(self.tileSize)
        self.do_bindings()
        self.clear()
        self.draw()
        self.radiobuttons.reset()

    def canvas_to_map_coordinates(self, xClick, yClick):
        return (xClick-2) // (self.tileSize+1), (yClick-2) // (self.tileSize+1)

    def clear_graphical_layers(self):
        overworld = app.App.instance.overworld
        for k, v in self.graphicalLayers.items():
            if v is not None:
                for imageId in v.flat:
                    self.canvas.delete(imageId)
            self.graphicalLayers[k] = -np.ones(
                getattr(overworld, k).shape, dtype=np.int16)

        self.currentGraphicalLayer = None
        print("Cleared graphical layers.")

    def draw_tile(self, x, y, tileId):
        xLayer, yLayer = self.currentLayer.shape
        tile = self.tiles[tileId]

        if 0 <= x < xLayer and 0 <= y < yLayer:
            self.currentLayer[x, y] = tileId

            if self.currentGraphicalLayer[x, y] != -1:
                self.canvas.delete(self.currentGraphicalLayer[x, y])

            self.currentGraphicalLayer[x, y] = self.canvas.create_image(
                2 + x * (self.tileSize + 1),
                2 + y * (self.tileSize + 1),
                image=tile,
                anchor="nw")

            self._reorder_stack(x, y)

    def draw_current_tile(self, xCanvas, yCanvas):
        x, y = self.canvas_to_map_coordinates(xCanvas, yCanvas)
        tileId = app.App.instance.tilesetFrame.selected_tile()
        if tileId is not None:
            self.draw_tile(x, y, tileId)

        self.canvas.hovered_cell = None
        self.draw_selection_rectangle(x, y)

    def draw_selection_rectangle(self, x, y):
        xLayer, yLayer = self.currentLayer.shape

        if 0 <= x < xLayer and 0 <= y < yLayer:
            self.canvas.delete(self.canvas.hover_rectangle)
            self.canvas.hovered_cell = (x, y)
            rectangle = (2 + x * (self.tileSize + 1),
                         2 + y * (self.tileSize + 1),
                         2 + (x + 1) * (self.tileSize + 1),
                         2 + (y + 1) * (self.tileSize + 1))
            self.canvas.hover_rectangle = self.canvas.create_rectangle(
                *rectangle, self.hover_style)

    def on_click_down_canvas(self, event):
        x = int(self.canvas.canvasx(event.x))
        y = int(self.canvas.canvasy(event.y))
        self.clicked = True
        self.draw_current_tile(x, y)

    def on_click_up_canvas(self, event):
        self.clicked = False

    def on_motion_canvas(self, event):
        xCanvas = int(self.canvas.canvasx(event.x))
        yCanvas = int(self.canvas.canvasy(event.y))
        x, y = self.canvas_to_map_coordinates(xCanvas, yCanvas)
        if self.clicked:
            self.draw_current_tile(xCanvas, yCanvas)
        elif (x, y) != self.canvas.hovered_cell:
            self.draw_selection_rectangle(x, y)

    def on_leave_canvas(self, event):
        self.canvas.delete(self.canvas.hover_rectangle)
        self.canvas.hover_rectangle = None
        self.canvas.hovered_tile = None

    def on_layer_selected(self, *_):
        selected_layer = self.radiobuttons.get()
        layer = self.labelToLayer[selected_layer]
        self.select_layer(layer)

    def select_layer(self, layer):
        self.currentLayer = getattr(app.App.instance.overworld, layer)
        self.currentGraphicalLayer = self.graphicalLayers[layer]
        print("Selected {}".format(layer))

    def _draw_grid(self):
        height, width = app.App.instance.overworld.shape
        canvasHeight = height * (self.tileSize + 1)
        canvasWidth = width * (self.tileSize + 1)

        for i in range(height + 1):
            step = 1 + i * (self.tileSize + 1)
            self.canvas.create_line(1, step, canvasWidth, step)

        for j in range(width + 1):
            step = 1 + j * (self.tileSize + 1)
            self.canvas.create_line(step, 1, step, canvasHeight)

    def _draw_map(self):
        print("Drawing map...")

        overworld = app.App.instance.overworld
        tileset = app.App.instance.tileset

        for layerName in ["lowerTiles", "upperTiles", "collisions"]:
            layer = getattr(overworld, layerName)
            self.select_layer(layerName)
            it = np.nditer(layer, flags=['multi_index'])
            while not it.finished:
                tileId = int(it[0])
                if tileId != -1:
                    self.draw_tile(*it.multi_index, tileId)
                it.iternext()

    def _reorder_stack(self, x, y):
        for layerName in self.labelToLayer.values():
            self.canvas.lift(self.graphicalLayers[layerName][x, y])

    def _configure(self):
        height, width = app.App.instance.overworld.shape
        self.canvas.config(width=1 + width * (self.tileSize + 1))
        self.canvas['scrollregion'] = self.canvas.bbox("all")
