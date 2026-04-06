import flet as ft

CARD_WIDTH = 70
CARD_HEIGHT = 100
CARD_OFFSET = 25
DROP_PROXIMITY = 40


class Card(ft.Container):
    def __init__(self, solitaire, suite, rank):
        super().__init__(
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            left=0,
            top=0,
        )

        self.solitaire = solitaire
        self.suite = suite
        self.rank = rank
        self.slot = None
        self.face_up = False
        self.draggable_pile = [self]

        self.card_image = ft.Image(
            src=f"/{self.solitaire.skin}",
            fit=ft.BoxFit.COVER,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
        )

        self.card_body = ft.Container(
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            border_radius=ft.border_radius.all(6),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=self.card_image,
        )

        self.gesture = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=5,
            on_pan_start=self.start_drag,
            on_pan_update=self.drag,
            on_pan_end=self.drop,
            on_tap=self.click,
            on_double_tap=self.double_click,
            content=self.card_body,
        )

        self.content = self.gesture

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
        self.card_image.src = f"/{self.rank.name}_{self.suite.name}.svg"
        self.update()

    def turn_face_down(self):
        self.face_up = False
        self.card_image.src = f"/{self.solitaire.skin}"
        self.update()

    def place(self, slot):
        pile = self.get_draggable_pile()
        old_slot = self.slot

        if old_slot is not None:
            self.solitaire.history.append(
                {
                    "cards": pile[:],
                    "from_slot": old_slot,
                    "to_slot": slot,
                    "score": self.solitaire.score,
                }
            )

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

        if old_slot in self.solitaire.tableau and old_slot.pile:
            top_card = old_slot.get_top_card()
            if top_card is not None and not top_card.face_up:
                top_card.turn_face_up()

        if slot in self.solitaire.foundations:
            self.solitaire.score += 10
            self.solitaire.score_text.value = f"Pontos: {self.solitaire.score}"

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

        base_left = self.left + e.local_delta.x
        base_top = self.top + e.local_delta.y

        for i, card in enumerate(self.draggable_pile):
            card.left = max(0, base_left)
            card.top = max(0, base_top) + i * CARD_OFFSET

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
                self.solitaire.draw_from_stock()

    def double_click(self, e):
        self.get_draggable_pile()

        if self.face_up and len(self.draggable_pile) == 1:
            self.move_on_top()
            for slot in self.solitaire.foundations:
                if self.solitaire.check_foundation_rules(self, slot):
                    self.place(slot)
                    return