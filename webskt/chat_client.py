import asyncio
import websockets

class Client:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)

    async def receive_messages(self):
        while True:
            try:
                response = await self.websocket.recv()
                print(f"Server response: {response}")
            except websockets.ConnectionClosed:
                print("Server disconnected")
                break

    async def send_messages(self):
        user_id = input("Enter your user ID: ")
        room_id = input("Enter the room ID to join: ")
        await self.websocket.send(f"User  {user_id}")
        await self.websocket.send(f"Join {room_id}")
        response = await self.websocket.recv()
        print(f"Server response: {response}")
        while True:
            message = input("Enter message to send to the server: ")
            await self.websocket.send(message)
            print(f"Sent: {message}")
            response = await self.websocket.recv()
            print(f"Server response: {response}")

    async def start(self):
        await self.connect()
        asyncio.create_task(self.receive_messages())
        await self.send_messages()

if __name__ == "__main__":
    server_url = input("Enter the WebSocket server URI (e.g., ws://<ngrok_url>): ")
    if not server_url.startswith("ws://") and not server_url.startswith("wss://"):
        print("Invalid WebSocket URL. Please use ws:// or wss://")
    else:
        client = Client(server_url)
        asyncio.run(client.start())