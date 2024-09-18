import asyncio
import websockets

# Function to send and receive messages from the WebSocket server
async def communicate_with_server(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter message to send to server: ")
            await websocket.send(message)
            print(f"Sent: {message}")

            response = await websocket.recv()
            print(f"Server response: {response}")

# Run the client
if __name__ == "__main__":
    server_url = input("Enter the WebSocket server URI (e.g., ws://<ngrok_url>): ")

    # Make sure the URI is correctly formatted
    if not server_url.startswith("ws://") and not server_url.startswith("wss://"):
        print("Invalid WebSocket URL. Please use ws:// or wss://")
    else:
        asyncio.get_event_loop().run_until_complete(communicate_with_server(server_url))
