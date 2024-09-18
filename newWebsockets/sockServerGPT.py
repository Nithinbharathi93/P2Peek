import asyncio
import websockets
from pyngrok import ngrok

# List to keep track of all connected clients
connected_clients = set()

# Function to handle incoming messages from clients
async def handle_client(websocket, path):
    # Add the new client to the set of connected clients
    connected_clients.add(websocket)
    print(f"Client connected from {path}")
    try:
        async for message in websocket:
            print(f"Message received: {message}")

            # Broadcast the message to all connected clients
            await broadcast_message(f"Broadcast: {message}")

    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        # Remove the client from the set when they disconnect
        connected_clients.remove(websocket)

# Function to broadcast a message to all connected clients
async def broadcast_message(message):
    if connected_clients:  # Check if there are any clients connected
        await asyncio.gather(*(client.send(message) for client in connected_clients))

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
