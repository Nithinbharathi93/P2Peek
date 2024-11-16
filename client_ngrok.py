import asyncio
import websockets
import sys

async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")
    except websockets.ConnectionClosed:
        print("Connection to server closed")

async def send_messages(websocket):
    try:
        while True:
            message = input("Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
            await websocket.send(message)
    except websockets.ConnectionClosed:
        print("Connection to server closed")

async def main():
    # Get the ngrok URL from user input
    server_url = input("Enter the ngrok URL (format: tcp://X.tcp.ngrok.io:XXXXX): ")
    
    # Convert ngrok TCP URL to WebSocket URL
    # Replace 'tcp://' with 'ws://'
    ws_url = server_url.replace('tcp://', 'ws://')

    try:
        async with websockets.connect(ws_url) as websocket:
            print("Connected to server!")
            
            # Create tasks for sending and receiving messages
            receive_task = asyncio.create_task(receive_messages(websocket))
            send_task = asyncio.create_task(send_messages(websocket))
            
            # Wait for either task to complete
            done, pending = await asyncio.wait(
                [receive_task, send_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel the remaining task
            for task in pending:
                task.cancel()
                
    except ConnectionRefusedError:
        print("Could not connect to the server")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient shutdown by user")