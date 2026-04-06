import random
import time
import threading
import flet as ft

from model import Suite, Rank
from slot import Slot
from card import Card

SOLITAIRE_WIDTH = 800
SOLITAIRE_HEIGHT = 600
TABLEAU_START_Y = 150
TABLEAU_GAP_X = 100
FOUNDATION_START_X = 300
TOP_Y = 10


class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()

        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT
        self.controls = []

        self.cards = []
        self.foundations = []
        self.tableau = []

        self.stock = None
        self.waste = None

        self.history = []
        self.score = 0
        self.skin = "card_back0.png"
        

        self.score_text = ft.Text(
            "Pontos: 0",
            color="white",
            weight=ft.FontWeight.BOLD,
        )
        self.timer_text = ft.Text(
            "Tempo: 00:00",
            color="white",
            weight=ft.FontWeight.BOLD,
        )

        self._seconds = 0
        self._timer_running = False
        self._timer_thread = None

    def did_mount(self):
        self.start_new_game()

    def will_unmount(self):
        self._timer_running = False

    def start_new_game(self):
        self._timer_running = False

        self.controls.clear()
        self.cards.clear()
        self.foundations.clear()
        self.tableau.clear()
        self.stock = None
        self.waste = None
        self.history.clear()

        self.score = 0
        self.score_text.value = "Pontos: 0"

        self._seconds = 0
        self.timer_text.value = "Tempo: 00:00"

        self.create_slots()
        self.create_card_deck()
        self.deal_cards()
        self.start_timer()
        self.update()

    def create_slots(self):
        self.stock = Slot(
            self,
            top=TOP_Y,
            left=0,
            border=ft.border.all(1, "white"),
        )

        self.waste = Slot(
            self,
            top=TOP_Y,
            left=100,
            border=ft.border.all(1, "white"),
        )

        x = FOUNDATION_START_X
        for _ in range(4):
            foundation = Slot(
                self,
                top=TOP_Y,
                left=x,
                border=ft.border.all(1, "white"),
            )
            self.foundations.append(foundation)
            x += TABLEAU_GAP_X

        x = 0
        for _ in range(7):
            tableau_slot = Slot(
                self,
                top=TABLEAU_START_Y,
                left=x,
                border=ft.border.all(1, "white"),
            )
            self.tableau.append(tableau_slot)
            x += TABLEAU_GAP_X

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundations)
        self.controls.extend(self.tableau)

    def create_card_deck(self):
        suites = [
            Suite("hearts", "RED"),
            Suite("diamonds", "RED"),
            Suite("clubs", "BLACK"),
            Suite("spades", "BLACK"),
        ]

        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]

        self.cards = [Card(self, suite, rank) for suite in suites for rank in ranks]

    def deal_cards(self):
        random.shuffle(self.cards)
        self.controls.extend(self.cards)

        remaining_cards = self.cards[:]
        first_slot = 0

        while first_slot < len(self.tableau):
            for slot in self.tableau[first_slot:]:
                card = remaining_cards.pop(0)
                card.place(slot)
            first_slot += 1

        for slot in self.tableau:
            top_card = slot.get_top_card()
            if top_card is not None:
                top_card.turn_face_up()

        for card in remaining_cards:
            card.place(self.stock)
            card.turn_face_down()

        self.update()

    def draw_from_stock(self):
        if self.stock is None or self.waste is None:
            return

        if len(self.stock.pile) == 0:
            self.restart_stock()
            return

        card = self.stock.get_top_card()
        if card is None:
            return

        card.move_on_top()
        card.place(self.waste)
        card.turn_face_up()
        self.update()

    def restart_stock(self):
        while len(self.waste.pile) > 0:
            card = self.waste.get_top_card()
            card.turn_face_down()
            card.move_on_top()
            card.place(self.stock)

        self.update()

    def check_tableau_rules(self, card, slot):
        top_card = slot.get_top_card()

        if top_card is not None:
            return (
                card.suite.color != top_card.suite.color
                and card.rank.value == top_card.rank.value - 1
                and top_card.face_up
            )
        return card.rank.name == "King"

    def check_foundation_rules(self, card, slot):
        top_card = slot.get_top_card()

        if top_card is None:
            return card.rank.name == "Ace"

        return (
            card.suite.name == top_card.suite.name
            and card.rank.value == top_card.rank.value + 1
        )

    def check_win(self):
        total = sum(len(slot.pile) for slot in self.foundations)
        return total == 52

    def winning_sequence(self):
        for slot in self.foundations:
            for card in slot.pile:
                card.move_on_top()
                card.top = random.randint(0, SOLITAIRE_HEIGHT - 100)
                card.left = random.randint(0, SOLITAIRE_WIDTH - 70)

        self.update()

        dlg = ft.AlertDialog(title=ft.Text("Parabéns! Você venceu!"))
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def change_skin(self, skin_name):
        self.skin = skin_name
        for card in self.cards:
            if not card.face_up:
                card.card_image.src = f"/{self.skin}"
        self.update()

    def undo_move(self, e=None):
        if not self.history:
            return

        last_move = self.history.pop()
        moved_cards = last_move["cards"]
        from_slot = last_move["from_slot"]
        to_slot = last_move["to_slot"]
        old_score = last_move["score"]

        for card in reversed(moved_cards):
            if card in to_slot.pile:
                to_slot.pile.remove(card)

        for card in moved_cards:
            card.slot = from_slot
            from_slot.pile.append(card)
            card.left = from_slot.left
            if from_slot in self.tableau:
                card.top = from_slot.top + (from_slot.pile.index(card) * 25)
            else:
                card.top = from_slot.top

        self.score = old_score
        self.score_text.value = f"Pontos: {self.score}"
        self.update()

    def restart_game(self, e=None):
        self.start_new_game()

    def toggle_theme(self, page):
        if page.bgcolor == ft.Colors.GREEN_800:
            page.bgcolor = ft.Colors.GREY_900
            if page.appbar is not None:
                page.appbar.bgcolor = ft.Colors.BLACK87
        else:
            page.bgcolor = ft.Colors.GREEN_800
            if page.appbar is not None:
                page.appbar.bgcolor = ft.Colors.GREEN_900

        page.update()

    def new_random_game(self, e=None):
        self.start_new_game()

    def start_timer(self):
        self._timer_running = False
        time.sleep(0.05)
        self._timer_running = True

        def run_timer():
            while self._timer_running:
                time.sleep(1)
                self._seconds += 1
                minutes = self._seconds // 60
                seconds = self._seconds % 60
                self.timer_text.value = f"Tempo: {minutes:02}:{seconds:02}"
                try:
                    self.update()
                except Exception:
                    break

        self._timer_thread = threading.Thread(target=run_timer, daemon=True)
        self._timer_thread.start()