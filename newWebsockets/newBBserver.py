import asyncio
import websockets
from pyngrok import ngrok
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to handle incoming messages from clients
async def handle_client(websocket, path):
    try:
        # Validate the path
        if not path.startswith("/"):
            logging.warning(f"Invalid path: {path}")
            return

        # Handle incoming messages
        async for message in websocket:
            try:
                # Validate the message
                if not isinstance(message, str):
                    logging.warning(f"Invalid message: {message}")
                    continue

                # Process the message
                logging.info(f"Message received: {message}")
                await websocket.send(f"Server response: {message}")
            except Exception as e:
                logging.error(f"Error processing message: {e}")
    except websockets.ConnectionClosed:
        logging.info("Client disconnected")
    except Exception as e:
        logging.error(f"Error handling client: {e}")

# Main function to start the WebSocket server
async def start_server():
    port = 8765  # Define the port number
    server = await websockets.serve(handle_client, "0.0.0.0", port)
    logging.info(f"WebSocket server started on ws://localhost:{port}")
    token = "2ly0aXUlC9KdEJovwEKz5In1HNz_42Q35noMSzAUHAdm7FUyb"
    ngrok.set_auth_token(token)
    
    # Open the server to the internet using ngrok HTTP tunnel
    http_tunnel = ngrok.connect(port)
    public_url = http_tunnel.public_url.replace("http", "ws")
    logging.info(f"ngrok tunnel opened: {public_url}")

    # Keep the server running
    try:
        await server.wait_closed()
    except KeyboardInterrupt:
        logging.info("Server shut down")
    except Exception as e:
        logging.error(f"Error running server: {e}")

# Run the server
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server())