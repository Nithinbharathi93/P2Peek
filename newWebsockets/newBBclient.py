import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core.control_event import ControlEvent
import asyncio
import websockets

class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            Column(
                [
                    Text(message.user_name, weight="bold"),
                    Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "Unknown"  # or any default value you prefer

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

async def websocket_client(page: ft.Page, uri, user_name, room_id, chat):
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(user_name)
            await websocket.send(room_id)

            async def receive_messages():
                while True:
                    try:
                        message_recv = await websocket.recv()
                        if not message_recv.startswith("<"):
                            message = Message(user_name=user_name, text=f"{message_recv}", message_type="login_message")
                        else:
                            message_proc = message_recv[1:].partition("> ")
                            message = Message(user_name=message_proc[0], text=message_proc[2], message_type="chat_message")
                        on_message(page, message, chat)
                    except websockets.ConnectionClosedOK:
                        print("WebSocket connection closed normally.")
                        break
                    except websockets.ConnectionClosedError:
                        print("WebSocket connection closed due to an error.")
                        break
                    except Exception as e:
                        print(f"Error receiving message: {e}")
                        break

            await receive_messages()
    except Exception as e:
        print(f"WebSocket connection error: {e}")

def on_message(page: ft.Page, message: Message, chat):
    if message.message_type == "chat_message":
        m = ChatMessage(message)
    elif message.message_type == "login_message":
        m = Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
    chat.controls.append(m)
    page.update()

async def send_message(websocket, message_text, user_name, page, chat):
    try:
        message_to_send = f"<{user_name}> {message_text}"
        await websocket.send(message_to_send)
        on_message(page, Message(user_name=user_name, text=message_text, message_type="chat_message"), chat)
    except Exception as e:
        print(f"Error sending message: {e}")

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "P2Peek"
    page.theme_mode = ft.ThemeMode.LIGHT

    websocket = None

    def join_chat_click(e: ControlEvent):
        nonlocal websocket
        if not all([username:=join_user_name.value, room_id:=join_room_id.value, (join_chk or (servip:=join_pass_code))]):
            if not join_user_name.value:
                join_user_name.error_text = "Name cannot be blank!"
                join_user_name.update()
            if not join_room_id.value:
                join_room_id.error_text = "Room Id cannot be blank!"
                join_room_id.update()
            if (not join_pass_code.value) and (not join_chk.value) :
                join_pass_code.error_text = "Passcode cannot be blank!"
                join_pass_code.update()
                
        else:
            if join_chk.value:
                uri = "ws://localhost:8765"
            else:
                uri = join_pass_code.value
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"{join_user_name.value} has joined the chat.",
                    message_type="login_message",
                )
            )
            page.update()
            page.controls.append(ft.ProgressRing())
            page.update()
        asyncio.create_task(websocket_client(page, uri, username, room_id, chat))
        nonlocal websocket
        if not all([username:=join_user_name.value, room_id:=join_room_id.value, (join_chk or (servip:=join_pass_code))]):
            if not join_user_name.value:
                join_user_name.error_text = "Name cannot be blank!"
                join_user_name.update()
            if not join_room_id.value:
                join_room_id.error_text = "Room Id cannot be blank!"
                join_room_id.update()
            if (not join_pass_code.value) and (not join_chk.value) :
                join_pass_code.error_text = "Passcode cannot be blank!"
                join_pass_code.update()
                
        else:
            if join_chk.value:
                uri = "ws://localhost:8765"
            else:
                uri = join_pass_code.value
            asyncio.create_task(websocket_client(page, uri, username, room_id, chat))
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"{join_user_name.value} has joined the chat.",
                    message_type="login_message",
                )
            )
            page.update()

    def send_message_click(e):
        nonlocal websocket
        if new_message.value != "":
            asyncio.create_task(send_message(websocket, new_message.value, page.session.get("user_name"), page, chat))
            new_message.value = ""
            new_message.focus()
            page.update()

    def design(e: ControlEvent):
        if join_chk.value:
            join_pass_code.value = None
            join_pass_code.disabled = True
        else:
            join_pass_code.disabled = False
        
        page.update()
    
    # A dialog asking for a user display name
    join_user_name = TextField(
        label="Username",
        autofocus=True,
        on_submit=join_chat_click,
    )
    join_room_id = TextField(
        label="Room Id",
        password=True,
        on_submit=join_chat_click,
    )
    join_pass_code = TextField(
        label="Passcode",
        on_submit=join_chat_click,
    )
    join_chk = Checkbox(
        label="Server",
        value=False,
        on_change=design
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=Text("Welcome!"),
        content=Column([join_user_name, join_room_id, join_pass_code, join_chk], width=300, height=220, tight=True),
        actions=[ElevatedButton(text="Join chat", on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add everything to the page
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )

ft.app(target=main)