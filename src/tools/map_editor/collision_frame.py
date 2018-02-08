import tkinter as tk

from core.overworld import CollisionMask
from utils import EnumPanel


class CollisionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.collisionPanel = EnumPanel(self, CollisionMask, orient=tk.VERTICAL)

        self.collisionPanel.pack(side=tk.TOP)
