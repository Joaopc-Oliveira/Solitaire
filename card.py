import random
import flet as ft

CARD_WIDTH = 70
CARD_HEIGHT = 100
CARD_OFFSET = 25
DROP_PROXIMITY = 20


class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, rank):
        super().__init__()

        self.solitaire = solitaire
        self.suite = suite
        self.rank = rank

        self.slot = None
        self.face_up = False
        self.draggable_pile = [self]

        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 5

        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.drop
        self.on_tap = self.click
        self.on_double_tap = self.double_click

        self.content = ft.Container(
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            border_radius=ft.border_radius.all(6),
            content=ft.Image(
                src="card_back.png",
                fit=ft.BoxFit.COVER
            ),
        )

    def get_draggable_pile(self):
        if (
            self.slot is not None
            and self.slot != self.solitaire.stock
            and self.slot != self.solitaire.waste
        ):
            index = self.slot.pile.index(self)
            self.draggable_pile = self.slot.pile[index:]
        else:
            self.draggable_pile = [self]

        return self.draggable_pile

    def move_on_top(self):
        pile = self.get_draggable_pile()

        for card in pile:
            if card in self.solitaire.controls:
                self.solitaire.controls.remove(card)
                self.solitaire.controls.append(card)

        self.solitaire.update()

    def turn_face_up(self):
        self.face_up = True
        self.content.content = ft.Image(
            src=f"{self.rank.name}_{self.suite.name}.svg",
            fit=ft.BoxFit.COVER,
        )
        self.solitaire.update()

    def turn_face_down(self):
        self.face_up = False
        self.content.content = ft.Image(
            src="card_back.png",
            fit=ft.BoxFit.COVER,
        )
        self.solitaire.update()

    def place(self, slot):
        pile = self.get_draggable_pile()
        old_slots = []

        for card in pile:
            old_slots.append(card.slot)

        for card in pile:
            if card.slot is not None and card in card.slot.pile:
                card.slot.pile.remove(card)

            card.slot = slot

            if slot in self.solitaire.tableau:
                card.top = slot.top + len(slot.pile) * CARD_OFFSET
            else:
                card.top = slot.top

            card.left = slot.left
            slot.pile.append(card)

        for old_slot in old_slots:
            if old_slot in self.solitaire.tableau:
                top_card = old_slot.get_top_card()
                if top_card is not None and not top_card.face_up:
                    top_card.turn_face_up()

        if self.solitaire.check_win():
            self.solitaire.winning_sequence()

        self.solitaire.update()

    def bounce_back(self):
        pile = self.get_draggable_pile()

        for card in pile:
            if card.slot is not None:
                if card.slot in self.solitaire.tableau:
                    card.top = card.slot.top + card.slot.pile.index(card) * CARD_OFFSET
                else:
                    card.top = card.slot.top

                card.left = card.slot.left

        self.solitaire.update()

    def start_drag(self, e: ft.DragStartEvent):
        if self.face_up:
            self.get_draggable_pile()
            self.move_on_top()

    def drag(self, e: ft.DragUpdateEvent):
        if not self.face_up:
            return

        for i, card in enumerate(self.draggable_pile):
            card.top = max(0, self.top + e.local_delta.y) + i * CARD_OFFSET
            card.left = max(0, self.left + e.local_delta.x)

        self.solitaire.update()

    def drop(self, e: ft.DragEndEvent):
        if not self.face_up:
            self.bounce_back()
            return

        for slot in self.solitaire.tableau:
            target_top = slot.top + len(slot.pile) * CARD_OFFSET
            if (
                abs(self.top - target_top) < DROP_PROXIMITY
                and abs(self.left - slot.left) < DROP_PROXIMITY
                and self.solitaire.check_tableau_rules(self, slot)
            ):
                self.place(slot)
                return

        if len(self.draggable_pile) == 1:
            for slot in self.solitaire.foundations:
                if (
                    abs(self.top - slot.top) < DROP_PROXIMITY
                    and abs(self.left - slot.left) < DROP_PROXIMITY
                    and self.solitaire.check_foundation_rules(self, slot)
                ):
                    self.place(slot)
                    return

        self.bounce_back()

    def click(self, e):
        if self.slot is not None and self.slot in self.solitaire.tableau:
            if not self.face_up and self == self.slot.get_top_card():
                self.turn_face_up()

        elif self.slot == self.solitaire.stock:
            if self == self.slot.get_top_card():
                self.move_on_top()
                self.place(self.solitaire.waste)
                self.turn_face_up()

    def double_click(self, e):
        self.get_draggable_pile()

        if self.face_up and len(self.draggable_pile) == 1:
            self.move_on_top()
            for slot in self.solitaire.foundations:
                if self.solitaire.check_foundation_rules(self, slot):
                    self.place(slot)
                    return