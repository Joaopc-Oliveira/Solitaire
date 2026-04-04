import flet as ft

SLOT_WIDTH = 70
SLOT_HEIGHT = 100


class Slot(ft.Container):
    def __init__(self, solitaire, top: int, left: int, border=None):
        super().__init__()
        self.solitaire = solitaire
        self.pile = []

        self.top = top
        self.left = left
        self.width = SLOT_WIDTH
        self.height = SLOT_HEIGHT
        self.border = border
        self.border_radius = ft.border_radius.all(6)
        self.bgcolor = None
        self.on_click = self.click

    def get_top_card(self):
        if self.pile:
            return self.pile[-1]
        return None

    def click(self, e):
        if self == self.solitaire.stock and len(self.solitaire.stock.pile) == 0:
            self.solitaire.restart_stock()