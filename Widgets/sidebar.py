import flet as ft

rail = ft.NavigationRail(
    selected_index=0,
    label_type=ft.NavigationRailLabelType.ALL,
    # extended=True,
    min_width=50,
    min_extended_width=400,
    leading=ft.FloatingActionButton(icon=ft.icons.CREATE),
    group_alignment=-0.9,
    destinations=[
        ft.NavigationRailDestination(
            icon=ft.icons.CHAT,
            selected_icon_content=ft.Icon(ft.icons.CHAT),
            label_content=ft.Text("prompt"),
        ),
        ft.NavigationRailDestination(
            icon=ft.icons.SETTINGS_OUTLINED,
            selected_icon_content=ft.Icon(ft.icons.SETTINGS),
            label_content=ft.Text("Settings"),
        ),
    ],
    on_change=lambda e: print("Selected destination:", e.control.selected_index),
)
