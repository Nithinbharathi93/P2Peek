import asyncio
import websockets
from collections import defaultdict as df
from pyngrok import ngrok
class Server:
    def __init__(self):
        self.rooms = df(list)  # Dictionary to hold room_id and list of clients
    async def accept_connections(self, websocket, path):
        try:
            # Receive user ID and room ID from the client
            user_id = await websocket.recv()
            user_id = user_id.replace("User ", "")
            room_id = await websocket.recv()
            room_id = room_id.replace("Join ", "")
            # Check if the room already exists
            if room_id not in self.rooms:
                await websocket.send("New Group created")
            else:
                await websocket.send("Welcome to chat room")
            # Add the new connection to the room
            self.rooms[room_id].append(websocket)
            print(f"User {user_id} joined room {room_id}")
            # Start listening for messages from the client
            await self.client_handler(websocket, user_id, room_id)        
        except websockets.ConnectionClosed:
            print(f"Connection closed for user {user_id}")
            self.remove(websocket, room_id)
    async def client_handler(self, websocket, user_id, room_id):
        try:
            while True:
                message = await websocket.recv()
                print(f"Message received from {user_id}: {message}")
                if message:
                    message_to_send = f"<{user_id}> {message}"
                    await self.broadcast(message_to_send, websocket, room_id)
                else:
                    self.remove(websocket, room_id)
                    break
        except websockets.ConnectionClosed:
            print(f"User {user_id} disconnected")
            self.remove(websocket, room_id)
    async def broadcast(self, message_to_send, websocket, room_id):
        # Broadcast the message to all clients in the room except the sender
        for client in self.rooms[room_id]:
            if client != websocket:
                try:
                    await client.send(message_to_send)
                except websockets.ConnectionClosed:
                    self.remove(client, room_id)
    def remove(self, websocket, room_id):
        # Remove a websocket from the room if it's present
        if websocket in self.rooms[room_id]:
            self.rooms[room_id].remove(websocket)
            print(f"Client removed from room {room_id}")
async def main():
    server = Server()
    # Start the WebSocket server
    async with websockets.serve(server.accept_connections, "0.0.0.0", port:=8765):
        print("WebSocket server started on ws://localhost:8765")
        print(f"WebSocket server started on ws://localhost:{port}")
        token = "2ly0aXUlC9KdEJovwEKz5In1HNz_42Q35noMSzAUHAdm7FUyb"
        ngrok.set_auth_token(token)
        # Open the server to the internet using ngrok HTTP tunnel
        http_tunnel = ngrok.connect(port)
        public_url = http_tunnel.public_url.replace("http", "ws")
        print(f"ngrok tunnel opened: {public_url}")
        await asyncio.Future()  # Run the server until manually interrupted
if __name__ == "__main__":
    asyncio.run(main())