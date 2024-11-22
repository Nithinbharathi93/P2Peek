import asyncio
import websockets
import flet as ft
from flet_core.control_event import ControlEvent

# Global variable to store the websocket reference
websocket = None

# Chat message model
class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

# Chat message GUI component
class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                    ft.Text(message.text, selectable=True),
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


unm = ""  # Username will be set in the GUI
room_id = ""  # Room ID for the chat session
ws_link = ""  # WebSocket link to connect to

async def listen_to_server(websocket, page):
    while True:
        try:
            message = await websocket.recv()
            message = message.partition(":")
            page.pubsub.send_all(
                Message(
                    user_name=message[0],
                    text=message[2],
                    message_type="chat_message",
                )
            )
        except websockets.ConnectionClosed:
            page.pubsub.send_all(
                Message(
                    user_name="System",
                    text="Disconnected from the server.",
                    message_type="system_message",
                )
            )
            break

async def send_to_server(websocket, message, page):
    if websocket is None:
        page.pubsub.send_all(
            Message(
                user_name="System",
                text="WebSocket is not connected.",
                message_type="system_message",
            )
        )
        return  # Exit if websocket is not connected

    try:
        if message.lower() == 'quit':
            return
        await websocket.send(f"{unm}:{message}")
        page.pubsub.send_all(
            Message(
                user_name=unm,
                text=message,
                message_type="chat_message",
            )
        )
    except websockets.ConnectionClosed:
        page.pubsub.send_all(
            Message(
                user_name="System",
                text="Connection lost.",
                message_type="system_message",
            )
        )

async def chat_client(page):
    global websocket
    uri = ws_link  # Use the dynamic WebSocket link here

    try:
        async with websockets.connect(uri) as ws:
            websocket = ws  # Save the websocket reference here
            print(f"Connected to the server at {uri} for room {room_id}.")
            # Create two tasks and handle cancellation
            tasks = [
                asyncio.create_task(listen_to_server(websocket, page)),
            ]
            page.pubsub.subscribe(lambda msg: on_message(msg, page))  # Pass the page to on_message
            await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Connection failed: {e}")
        page.pubsub.send_all(
            Message(
                user_name="System",
                text=f"Connection failed: {e}",
                message_type="system_message",
            )
        )

def on_message(message: Message, page):
    if message.message_type == "chat_message":
        m = ChatMessage(message)
    elif message.message_type == "system_message":
        m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
    chat.controls.append(m)
    page.update()

def main(page: ft.Page):
    page.title = "WebSocket Chat"
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.theme_mode = ft.ThemeMode.LIGHT

    def join_chat_click(e: ControlEvent):
        global unm, room_id, ws_link
        if join_user_name.value and join_room_id.value and join_pass_code.value:
            unm = join_user_name.value
            room_id = join_room_id.value
            ws_link = join_pass_code.value  # WebSocket URL to connect to
            page.dialog.open = False
            page.update()
            asyncio.run(chat_client(page))

    def send_message_click(e):
        message = new_message.value
        if message:
            asyncio.run(send_to_server(websocket, message, page))  # Use the global websocket reference
            new_message.value = ""
            new_message.focus()
            page.update()

    # A dialog asking for a user display name, room ID, and WS Link
    join_user_name = ft.TextField(
        label="Username",
        autofocus=True,
        on_submit=join_chat_click,
    )
    
    join_room_id = ft.TextField(
        label="Room ID",
        autofocus=True,
        on_submit=join_chat_click,
    )
    
    join_pass_code = ft.TextField(
        label="WS Link",
        autofocus=True,
        on_submit=join_chat_click,
    )
    
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Enter your Username, Room ID, and WS Link"),
        content=ft.Column([join_user_name, join_room_id, join_pass_code], width=300, height=220, tight=True),
        actions=[ft.ElevatedButton(text="Join Chat", on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Chat messages
    global chat
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = ft.TextField(
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
        ft.Row(
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
