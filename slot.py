import flet as ft

SLOT_WIDTH = 70
SLOT_HEIGHT = 100


class Slot(ft.Container):
    def __init__(self, solitaire, top, left, border=None):
        super().__init__(
            width=SLOT_WIDTH,
            height=SLOT_HEIGHT,
            left=left,
            top=top,
            border=border,
            border_radius=6,
        )
        self.pile = []
        self.solitaire = solitaire
        self.on_click = self.click

    def click(self, e):
        if self == self.solitaire.stock:
            self.solitaire.draw_from_stock()

    def get_top_card(self):
        if self.pile:
            return self.pile[-1]
        return None