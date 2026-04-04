import random
import flet as ft

from model import Suite, Rank
from slot import Slot
from card import Card

SOLITAIRE_WIDTH = 800
SOLITAIRE_HEIGHT = 600


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

    def did_mount(self):
        self.create_slots()
        self.create_card_deck()
        self.deal_cards()

    def create_slots(self):
        self.stock = Slot(
            self,
            top=0,
            left=0,
            border=ft.border.all(1, ft.Colors.WHITE),
        )

        self.waste = Slot(
            self,
            top=0,
            left=100,
        )

        x = 300
        for _ in range(4):
            foundation = Slot(
                self,
                top=0,
                left=x,
                border=ft.border.all(1, ft.Colors.WHITE),
            )
            self.foundations.append(foundation)
            x += 100

        x = 0
        for _ in range(7):
            tableau_slot = Slot(
                self,
                top=150,
                left=x,
            )
            self.tableau.append(tableau_slot)
            x += 100

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundations)
        self.controls.extend(self.tableau)

        self.update()

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

        self.cards = []
        for suite in suites:
            for rank in ranks:
                self.cards.append(Card(self, suite, rank))

    def deal_cards(self):
        random.shuffle(self.cards)
        self.controls.extend(self.cards)

        remaining_cards = self.cards[:]
        first_slot = 0

        while first_slot < len(self.tableau):
            for slot in self.tableau[first_slot:]:
                card = remaining_cards[0]
                card.place(slot)
                remaining_cards.remove(card)
            first_slot += 1

        for slot in self.tableau:
            top_card = slot.get_top_card()
            if top_card is not None:
                top_card.turn_face_up()

        for card in remaining_cards:
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
        else:
            return card.rank.name == "King"

    def check_foundation_rules(self, card, slot):
        top_card = slot.get_top_card()

        if top_card is None:
            return card.rank.name == "Ace"

        return (
            card.suite.name == top_card.suite.name
            and card.rank.value == top_card.rank.value + 1
        )

    def restart_stock(self):
        while len(self.waste.pile) > 0:
            card = self.waste.get_top_card()
            card.turn_face_down()
            card.move_on_top()
            card.place(self.stock)

        self.update()

    def check_win(self):
        total = 0
        for slot in self.foundations:
            total += len(slot.pile)
        return total == 52

    def winning_sequence(self):
        for slot in self.foundations:
            for card in slot.pile:
                card.animate_position = 1000
                card.move_on_top()
                card.top = random.randint(0, SOLITAIRE_HEIGHT - 100)
                card.left = random.randint(0, SOLITAIRE_WIDTH - 70)

        self.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Parabéns! Você venceu!")
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()