import asyncio
import websockets
import threading

async def receive_messages(websocket):
    # Keep listening for messages from the server
    try:
        async for message in websocket:
            print(f"Received: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Disconnected from server")

async def send_messages(websocket):
    # Keep sending user input to the server
    while True:
        message = input("Enter a message: ")
        await websocket.send(message)

async def main():
    # Connect to the server
    async with websockets.connect("ws://localhost:6789") as websocket:
        # Start receiving and sending messages concurrently
        receive_task = asyncio.create_task(receive_messages(websocket))
        send_task = asyncio.create_task(send_messages(websocket))
        
        # Wait for both tasks to finish
        await asyncio.gather(receive_task, send_task)

# Run the client in a separate thread
def run_client():
    asyncio.run(main())

if __name__ == "__main__":
    client_thread = threading.Thread(target=run_client)
    client_thread.start()
