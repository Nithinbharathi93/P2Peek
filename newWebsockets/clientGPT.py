import asyncio
import websockets
# Function to send and receive messages from the WebSocket server
async def communicate_with_server(uri):
    async with websockets.connect(uri) as websocket:
        # Get user details for initial connection
        user_id = input("Enter your user ID: ")
        room_id = input("Enter the room ID to join: ")
        # Send user ID and room ID to the server
        await websocket.send(f"User {user_id}")
        await websocket.send(f"Join {room_id}")
        # Wait for the server's response
        # Chat loop to send and receive messages
        while True:
            response = await websocket.recv()
            print(f"Server response: {response}")
            message = input("Enter message to send to the server: ")
            await websocket.send([user_id, room_id, message])
            print(f"Sent: {message}")
# Run the client
if __name__ == "__main__":
    server_url = input("Enter the WebSocket server URI (e.g., ws://<ngrok_url>): ")
    # Make sure the URI is correctly formatted
    if not server_url.startswith("ws://") and not server_url.startswith("wss://"):
        print("Invalid WebSocket URL. Please use ws:// or wss://")
    else:
        asyncio.get_event_loop().run_until_complete(communicate_with_server(server_url))
'''
sample link: wss://9e78-2409-40f4-2009-dff3-8f88-1e13-ba48-6b38.ngrok-free.app
9e78240940f42009dff38f881e13ba486b38
'''