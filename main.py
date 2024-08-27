import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core.control_event import ControlEvent
import socket
import time
import threading
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "P2Peek"
    page.theme_mode = ft.ThemeMode.LIGHT

    def join_chat_click(e: ControlEvent):
        global server
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
            # if join_chk.value:
            #     server.connect(("8.8.8.8", 80))
            #     ip_address = (server.getsockname()[0])
            #     server.close()
            #     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #     l = [(255-int(i))/10 for i in ip_address.split('.')]
            #     d = {i+1:j for i, j in enumerate("abcdefghijklmnopqrstuvwxyz")}
            #     enc = "".join([d[int(i)] for i in l])
            #     rest = "".join([d[int(str(i)[-1])] for i in l])
            #     code = "".join([i+j for i, j in zip(enc,rest)])
            #     print(code)
            #     server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # else:
            servip = join_pass_code.value
            enc2, rest2 = servip[::2], servip[1::2]
            d2 = {j:i for i, j in enumerate("abcdefghijklmnopqrstuvwxyz")}
            enc2_l = [d2[i] for i in enc2]
            rest2_l = [d2[i] for i in rest2]
            ip_l = ([(f"{i}{j}") for i, j in zip(enc2_l, rest2_l)])
            servip = '.'.join([str((int(255-(float(i))))) for i in ip_l])
            server.connect((servip, 12345))
            #-----------------------------------------------------------------------
            server.send(str.encode(username))
            time.sleep(0.1)
            server.send(str.encode(room_id))
            rcv = threading.Thread(target=receive)
            rcv.start()
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
            
    def receive():
        global fin_msg, server
        while True:
            try:
                message_recv = str(server.recv(1024).decode())
                
                print("Recieving ..!", message_recv)
                if not message_recv.startswith("<"):
                    if not message_recv:
                        break
                    Message(
                    user_name=join_user_name.value,
                    text=f"{message_recv}",
                    message_type="login_message",
                    )
                    # print(f"Just Recieved {message_recv}")
                else:
                    message_proc = message_recv[1:].partition("> ")
                    print(f"Recived '{message_proc[-1]}' from {message_proc[0]}")
                    message_conv = Message(user_name=message_proc[0], 
                                        text=message_proc[2],
                                        message_type="chat_message")
                    print("Sending the message:",message_conv.user_name, "From", 
                          message_conv.text)
                    on_message(message_conv)   

            except: 
                print("An error occured!") 
                print(Exception)
                server.close() 
                break
        page.update()


    def send_message_click(e):
        global fin_msg, server
        if new_message.value != "":
            page.pubsub.send_all(
                fin_msg := Message(
                    page.session.get("user_name"),
                    new_message.value,
                    message_type="chat_message",
                )
            )
            print("Sending :",new_message)
            while True:
                server.send((new_message.value).encode())
                break
            
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)
    
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