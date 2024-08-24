import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core.control_event import ControlEvent

def main(page: ft.Page):
    # Set the window size
    page.title = "Login Page"
    page.window_width = 400
    page.window_height = 300
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.horizontal_alignment=ft.MainAxisAlignment.CENTER
    page.window_resizable = False
    
    textUsername = TextField(label="Username", text_align=ft.TextAlign.LEFT, width=200)
    textRoomid = TextField(label="RoomID", text_align=ft.TextAlign.LEFT, width=200, password=True)
    textipaddr = TextField(label="Passcode", text_align=ft.TextAlign.LEFT, width=200)
    chkbx = Checkbox(label="Server", value=False)
    btnGo = ElevatedButton(text="Continue", width=200, disabled=True)
    
    def validate(e: ControlEvent):
        if all([textUsername.value, textRoomid.value, (bool(textipaddr.value) or bool(chkbx.value))]):
            btnGo.disabled = False
        else:
            btnGo.disabled = True
        if bool(chkbx.value):
            textipaddr.disabled = True
        else:
            textipaddr.disabled = False
        page.update()
    
    def submit(e: ControlEvent):
        print("Username :", textUsername.value)
        print("Roomid :", textRoomid.value)
        print("Passcode :", textipaddr.value or "Nil\nDesignation : Server")
        
        page.clean()
        page.add(
            Row(
                controls=[
                    Text(value=f"Welcome to P2Peek", size=20)
                ], 
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        
    chkbx.on_change = validate
    textUsername.on_change = validate
    textRoomid.on_change = validate
    textipaddr.on_change = validate
    btnGo.on_click = submit
    
    page.add(
        Row(
            controls=[
                Column(
                    [
                        textUsername, textRoomid, textipaddr, chkbx, btnGo
                    ]
                )
            ], 
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

# Run the Flet app
ft.app(target=main)
