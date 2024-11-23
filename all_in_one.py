import asyncio
import threading
import websockets
import pyperclip
import flet as ft
from flet_core.control_event import ControlEvent
from pyngrok import ngrok

# Server code
connected_clients = set()

async def broadcast(message, sender):
    disconnected_clients = set()
    for client in connected_clients:
        if client != sender:
            try:
                await client.send(message)
            except websockets.ConnectionClosed:
                disconnected_clients.add(client)
    connected_clients.difference_update(disconnected_clients)

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    print("A new client connected.")
    try:
        async for message in websocket:
            sender, _, content = message.partition(":")
            print(f"{sender}: {content}")
            await broadcast(message, websocket)
    except websockets.ConnectionClosed:
        print("A client disconnected.")
    finally:
        connected_clients.remove(websocket)

def start_server_with_ngrok(port=6789):
    async def main():
        print(f"Server running on ws://localhost:{port}")
        async with websockets.serve(handle_client, "localhost", port):
            await asyncio.Future()  # Run forever

    # Start the ngrok tunnel
    token = "2pEGLpToPOxign7V3HrJ3XMgEqu_42cUWxgMavHEGBCpkD26D"  # Replace with your ngrok auth token
    ngrok.set_auth_token(token)
    tunnel = ngrok.connect(port, "tcp")
    public_url = tunnel.public_url.replace("tcp", "ws")
    print(f"ngrok public WebSocket URL: {public_url}")

    threading.Thread(target=asyncio.run, args=(main(),), daemon=True).start()
    return public_url

class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

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
        return user_name[:1].capitalize() if user_name else "?"

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER, ft.colors.BLUE, ft.colors.BROWN, ft.colors.CYAN,
            ft.colors.GREEN, ft.colors.INDIGO, ft.colors.LIME, ft.colors.ORANGE,
            ft.colors.PINK, ft.colors.PURPLE, ft.colors.RED, ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

unm = ""
room_id = ""
ws_link = ""
websocket = None

async def listen_to_server(websocket, page):
    while True:
        try:
            message = await websocket.recv()
            sender, _, content = message.partition(":")
            page.pubsub.send_all(
                Message(user_name=sender, text=content, message_type="chat_message")
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
        return
    try:
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
    uri = ws_link
    try:
        async with websockets.connect(uri) as ws:
            websocket = ws
            tasks = [asyncio.create_task(listen_to_server(websocket, page))]
            page.pubsub.subscribe(lambda msg: on_message(msg, page))
            await asyncio.gather(*tasks)
    except Exception as e:
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

    def on_server_checkbox_change(e: ControlEvent):
        if join_server.value:
            public_url = start_server_with_ngrok()  # Start the server with ngrok
            join_pass_code.value = public_url  # Update the pass code field with the ngrok URL
            pyperclip.copy(public_url)  # Copy the public URL to clipboard
            page.snack_bar = ft.SnackBar(ft.Text("ngrok link copied to clipboard!"))
            page.snack_bar.open = True
            page.update()

    def join_chat_click(e: ControlEvent):
        global unm, room_id, ws_link
        if join_user_name.value and join_room_id.value and join_pass_code.value:
            unm = join_user_name.value
            room_id = join_room_id.value
            ws_link = join_pass_code.value

            # Close the dialog and update the page
            page.dialog.open = False
            page.update()  # Ensure UI updates first

            # Schedule the chat client coroutine
            def start_chat_client():
                asyncio.run(chat_client(page))  # Runs the coroutine safely

            threading.Thread(target=start_chat_client, daemon=True).start()

    def send_message_click(e):
        message = new_message.value
        if message:
            asyncio.run(send_to_server(websocket, message, page))
            new_message.value = ""
            new_message.focus()
            page.update()

    join_user_name = ft.TextField(label="Username", autofocus=True, on_submit=join_chat_click)
    join_room_id = ft.TextField(label="Room ID", on_submit=join_chat_click)
    join_pass_code = ft.TextField(label="WS Link", read_only=False, on_submit=join_chat_click)
    join_server = ft.Checkbox(label="Run as Server", value=False, on_change=on_server_checkbox_change)

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Join Chat"),
        content=ft.Column([join_user_name, join_room_id, join_pass_code, join_server], width=300, height=220, tight=True),
        actions=[ft.ElevatedButton(text="Join Chat", on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    global chat
    chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
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
    page.add(
        ft.Container(content=chat, expand=True, border_radius=5,
                     padding=10, border=ft.border.all(1, ft.colors.OUTLINE)),
        ft.Row([new_message, ft.IconButton(icon=ft.icons.SEND, on_click=send_message_click)]),
    )

ft.app(target=main, assets_dir="assets")
