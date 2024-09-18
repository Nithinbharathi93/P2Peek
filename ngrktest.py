import asyncio
import websockets
from pyngrok import ngrok
from collections import defaultdict as df
import time

class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class Server:
    def __init__(self):
        self.rooms = df(list)

    async def accept_connections(self, websocket, path):
        print(f"New connection from {path}")

        # Receive user and room information
        user_id = await websocket.recv()
        user_id = user_id.replace("User ", "")
        room_id = await websocket.recv()
        room_id = room_id.replace("Join ", "")

        if room_id not in self.rooms:
            await websocket.send("New Group created")
        else:
            await websocket.send("Welcome to chat room")

        self.rooms[room_id].append(websocket)
        print(f"Connection added to the room {room_id}")

        # Start receiving messages
        while True:
            try:
                message = await websocket.recv()

                if message:
                    print(f"The message: {message}")
                    if message == "FILE":
                        await self.broadcastFile(websocket, room_id, user_id)
                    else:
                        message_to_send = f"<{user_id}> {message}"
                        await self.broadcast(message_to_send, websocket, room_id)

                else:
                    await self.remove(websocket, room_id)
                    break
            except websockets.ConnectionClosed:
                print(f"Connection with {user_id} closed")
                await self.remove(websocket, room_id)
                break

    async def broadcastFile(self, websocket, room_id, user_id):
        file_name = await websocket.recv()
        lenOfFile = await websocket.recv()

        # Notify other clients about the file
        for client in self.rooms[room_id]:
            if client != websocket:
                try:
                    await client.send("FILE")
                    await asyncio.sleep(0.1)
                    await client.send(file_name)
                    await asyncio.sleep(0.1)
                    await client.send(lenOfFile)
                    await asyncio.sleep(0.1)
                    await client.send(user_id)
                except:
                    await self.remove(client, room_id)

        # Handle file data transfer
        total = 0
        print(f"Receiving file: {file_name} of size {lenOfFile}")
        while str(total) != lenOfFile:
            data = await websocket.recv()
            total += len(data)
            for client in self.rooms[room_id]:
                if client != websocket:
                    try:
                        await client.send(data)
                    except:
                        await self.remove(client, room_id)
        print("File sent to all clients")

    async def broadcast(self, message_to_send, websocket, room_id):
        for client in self.rooms[room_id]:
            if client != websocket:
                try:
                    await client.send(message_to_send)
                except:
                    await self.remove(client, room_id)

    async def remove(self, websocket, room_id):
        if websocket in self.rooms[room_id]:
            self.rooms[room_id].remove(websocket)

async def main():
    port = 8765
    server = Server()

    # Expose the WebSocket server using ngrok
    ngrok_tunnel = ngrok.connect(port, "http")
    print(f"Publicly accessible WebSocket server URL: {ngrok_tunnel.public_url}")

    async with websockets.serve(server.accept_connections, "0.0.0.0", port):
        print(f"WebSocket server started on ws://localhost:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
