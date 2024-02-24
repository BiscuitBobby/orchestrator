import flet as ft
from flet import TextStyle

from Secrets.keys import user


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold", no_wrap=False),
                    ft.Markdown(message.text, code_theme="atom-one-dark", code_style=TextStyle(font_family="RobotoMono-VariableFont_wght.ttf"), selectable=True),
                ],
                tight=True,
                spacing=10,
                width=500
            ),
        ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Unknown"

    def get_avatar_color(self, user_name: str):
        if user_name == user:
            return ft.colors.BLUE
        else:
            return ft.colors.GREEN
