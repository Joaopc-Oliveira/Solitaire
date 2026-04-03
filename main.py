import flet as ft
from solitaire import Solitaire


def main(page: ft.Page):
    page.title = "Solitaire"
    page.window_width = 1000
    page.window_height = 700
    page.padding = 20
    page.bgcolor = ft.Colors.GREEN_700

    game = Solitaire()
    page.add(game)


ft.run(main, assets_dir="images")
