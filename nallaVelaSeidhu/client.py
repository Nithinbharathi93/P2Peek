# client.py
import asyncio
import websockets

async def listen_to_server(websocket):
    while True:
        try:
            message = await websocket.recv()
            print(f"\n[Server]: {message}")
        except websockets.ConnectionClosed:
            print("Disconnected from the server.")
            break

async def send_to_server(websocket):
    while True:
        try:
            # Use asyncio to handle input asynchronously
            message = await asyncio.get_event_loop().run_in_executor(None, input, "You: ")
            if message.lower() == 'quit':
                break
            await websocket.send(message)
        except websockets.ConnectionClosed:
            break

async def chat_client():
    uri = "ws://localhost:6789"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to the server.")
            # Create two tasks and handle cancellation
            tasks = [
                asyncio.create_task(listen_to_server(websocket)),
                asyncio.create_task(send_to_server(websocket))
            ]
            try:
                await asyncio.gather(*tasks)
            except asyncio.CancelledError:
                for task in tasks:
                    task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(chat_client())
