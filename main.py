import builtins
from Widgets.chat import *
from Widgets.sidebar import rail
from agent import agent_executor
import flet as ft


def main(page: ft.Page):
    builtins.global_prompt = ''
    page.window_width = 600
    page.window_height = 800
    page.window_min_width = 520
    page.title = "Orchestrator"

    def send_message_click(e):
        if new_message.value != "":

            builtins.global_prompt = new_message.value

            page.pubsub.send_all(Message(user, new_message.value, message_type="chat_message"))
            new_message.value = ""
            new_message.focus()
            page.update()

            try:
                new_message.read_only, new_message.autofocus = True, False
                new_message.hint_text = "generating output"
                page.update()

                output = agent_executor.invoke({f"input": {builtins.global_prompt}})["output"]
                new_message.read_only, new_message.autofocus = False, True
                new_message.hint_text = "Enter prompt..."

                page.pubsub.send_all(Message("Agent", output, message_type="chat_message"))
                new_message.focus()
                page.update()
                for message in chat.controls:
                    print(message)

            except Exception as e:
                page.pubsub.send_all(Message("Agent", f"an error has occured:\n{e}", message_type="chat_message"))
                new_message.read_only, new_message.autofocus = False, True
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
                                tooltip="Send prompt",
                                on_click=send_message_click,
                            ),
                        ]
                    ), ], alignment=ft.MainAxisAlignment.START, expand=True)
            ],
            expand=True,
        )
    )


ft.app(target=main)

try:
    del builtins.global_prompt
except Exception as e:
    print(e)
