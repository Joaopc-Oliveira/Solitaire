import flet as ft
from solitaire import Solitaire


def main(page: ft.Page):
    page.title = "Solitaire Pro"
    page.bgcolor = ft.Colors.GREEN_800
    page.window_width = 1100
    page.window_height = 850
    page.padding = 10

    high_score = 0
    try:
        if hasattr(page, "client_storage"):
            stored = page.client_storage.get("highscore")
            high_score = stored if stored is not None else 0
    except Exception:
        print("Aviso: client_storage não disponível.")

    game = Solitaire()

    try:
        if hasattr(page, "client_storage"):
            saved_score = page.client_storage.get("score")
            saved_seconds = page.client_storage.get("seconds")
            saved_skin = page.client_storage.get("skin")

            if saved_score is not None:
                game.score = saved_score
                game.score_text.value = f"Pontos: {saved_score}"

            if saved_seconds is not None:
                game._seconds = saved_seconds
                minutes = saved_seconds // 60
                seconds = saved_seconds % 60
                game.timer_text.value = f"Tempo: {minutes:02}:{seconds:02}"

            if saved_skin is not None:
                game.skin = saved_skin
    except Exception:
        pass

    high_score_text = ft.Text(
        f"Recorde: {high_score}",
        color="gold",
        weight=ft.FontWeight.BOLD,
    )

    def save_state(e):
        nonlocal high_score

        try:
            if hasattr(page, "client_storage"):
                page.client_storage.set("score", game.score)
                page.client_storage.set("seconds", game._seconds)
                page.client_storage.set("skin", game.skin)

                if game.score > high_score:
                    page.client_storage.set("highscore", game.score)
                    high_score = game.score
                    high_score_text.value = f"Recorde: {high_score}"

            page.open(ft.SnackBar(content=ft.Text("Estado guardado!")))
            page.update()

        except Exception:
            page.open(ft.SnackBar(content=ft.Text("Erro ao guardar.")))
            page.update()

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.STYLE),
        title=ft.Row(
            controls=[
                game.score_text,
                ft.VerticalDivider(),
                game.timer_text,
                ft.VerticalDivider(),
                high_score_text,
            ],
            spacing=20,
        ),
        bgcolor=ft.Colors.GREEN_900,
        actions=[
            ft.IconButton(
                icon=ft.Icons.LOOKS_ONE,
                data="card_back0.png",
                on_click=lambda e: game.change_skin(e.control.data),
                tooltip="Verso 1",
            ),
            ft.IconButton(
                icon=ft.Icons.LOOKS_TWO,
                data="card_back1.png",
                on_click=lambda e: game.change_skin(e.control.data),
                tooltip="Verso 2",
            ),
            ft.IconButton(
                icon=ft.Icons.LOOKS_3,
                data="card_back2.png",
                on_click=lambda e: game.change_skin(e.control.data),
                tooltip="Verso 3",
            ),
            ft.IconButton(
                icon=ft.Icons.LOOKS_4,
                data="card_back3.png",
                on_click=lambda e: game.change_skin(e.control.data),
                tooltip="Verso 4",
            ),
            ft.IconButton(
                icon=ft.Icons.DARK_MODE,
                on_click=lambda e: game.toggle_theme(page),
                tooltip="Tema dark/light",
            ),
            ft.TextButton(
                content="Novo Jogo",
                icon=ft.Icons.CASINO,
                on_click=game.new_random_game,
            ),
            ft.TextButton(
                content="Desfazer",
                icon=ft.Icons.UNDO,
                on_click=game.undo_move,
            ),
            ft.TextButton(
                content="Reiniciar",
                icon=ft.Icons.REFRESH,
                on_click=game.restart_game,
            ),
            ft.IconButton(
                icon=ft.Icons.SAVE,
                on_click=save_state,
                tooltip="Guardar estado",
            ),
        ],
    )

    page.add(game)
    page.update()


if __name__ == "__main__":
    ft.run(
        main,
        assets_dir="images",
        view=ft.AppView.WEB_BROWSER,
        port=8000,
        host="0.0.0.0",
    )