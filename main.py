import builtins

from Widgets.sidebar import rail
from agent import agent_executor
import flet as ft

user = "BiscuitBobby"

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
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=10,
                width=500 # text width
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

def main(page: ft.Page):
    page.window_width = 600
    page.window_height = 800
    page.title = "Orchestrator"

    def send_message_click(e):
        if new_message.value != "":

            builtins.global_prompt = new_message.value

            page.pubsub.send_all(Message(user, new_message.value, message_type="chat_message"))
            new_message.value = ""
            new_message.focus()
            page.update()

            try:
                print("generating output")
                output = agent_executor.invoke({f"input": {builtins.global_prompt}})["output"]
                print(output)
                page.pubsub.send_all(Message("Agent", output, message_type="chat_message"))
                new_message.value = ""
                new_message.focus()
                page.update()

            except Exception as e:
                page.pubsub.send_all(Message("Agent", f"an error has occured:\n{e}", message_type="chat_message"))
                new_message.value = ""
                new_message.focus()
                page.update()

    def on_message(message: Message):
        m = ChatMessage(message)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = ft.TextField(
        hint_text="Enter prompt...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=None,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add everything to the page
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([
                ft.Container(
                    content=chat,
                    border=ft.border.all(1, ft.colors.OUTLINE),
                    border_radius=5,
                    padding=10,
                    expand=True,
                ),
                ft.Row(
                    [
                        new_message,
                        ft.IconButton(
                            icon=ft.icons.SEND_ROUNDED,
                            tooltip="Prompt",
                            on_click=send_message_click,
                        ),
                    ]
                ),], alignment=ft.MainAxisAlignment.START, expand=True)
            ],
            expand=True,
        )
    )


ft.app(target=main)
