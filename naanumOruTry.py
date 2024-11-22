import asyncio
import websockets

async def handle_client(websocket, path):
    print("Client connected")
    await websocket.send("Hello from the server!")
    await websocket.close()

async def main():
    print("Server running on ws://localhost:6789")
    async with websockets.serve(handle_client, "localhost", 6789):
        await asyncio.Future()  # Run forever

asyncio.run(main())
