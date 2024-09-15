

import asyncio
import websockets
from pyngrok import ngrok

# Function to handle incoming messages from clients
async def handle_client(websocket, path):
    print(f"Client connected from {path}")
    try:
        async for message in websocket:
            print(f"Message received: {message}")
            await websocket.send(f"Server response: {message}")
    except websockets.ConnectionClosed:
        print("Client disconnected")

# Main function to start the WebSocket server
async def start_server():
    port = 8765  # Define the port number
    server = await websockets.serve(handle_client, "0.0.0.0", port)
    print(f"WebSocket server started on ws://localhost:{port}")

    token = "2ly0aXUlC9KdEJovwEKz5In1HNz_42Q35noMSzAUHAdm7FUyb"
    ngrok.set_auth_token(token)
    
    # Open the server to the internet using ngrok HTTP tunnel
    http_tunnel = ngrok.connect(port)
    public_url = http_tunnel.public_url.replace("http", "ws")
    print(f"ngrok tunnel opened: {public_url}")

    # Keep the server running
    await server.wait_closed()

# Run the server
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server())
