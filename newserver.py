# server.py
import asyncio
import websockets

connected_clients = set()

async def broadcast(message, sender):
    disconnected_clients = set()
    for client in connected_clients:
        if client != sender:
            try:
                await client.send(message)
            except websockets.ConnectionClosed:
                disconnected_clients.add(client)
    
    # Remove disconnected clients
    connected_clients.difference_update(disconnected_clients)

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    print("A new client connected.")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await broadcast(message, websocket)
    except websockets.ConnectionClosed:
        print("A client disconnected.")
    finally:
        connected_clients.remove(websocket)

start_server = websockets.serve(handle_client, "localhost", 6789)

print("Server running on ws://localhost:6789")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
