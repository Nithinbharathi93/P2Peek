import asyncio
import websockets
import threading

# A set to store all connected clients
clients = set()

async def handle_client(websocket):
    # Register the new client
    clients.add(websocket)
    try:
        # Keep listening for messages from the client
        async for message in websocket:
            # Broadcast the received message to all connected clients
            await broadcast(message)
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        # Unregister the client
        clients.remove(websocket)

async def broadcast(message):
    # Send the message to all connected clients
    if clients:
        await asyncio.wait([client.send(message) for client in clients])

async def main():
    # Start the server
    async with websockets.serve(handle_client, "localhost", 6789):
        print("Server started on ws://localhost:6789")
        await asyncio.Future()  # Run forever

# Run the server in a separate thread
def run_server():
    # Create and run the event loop manually
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

