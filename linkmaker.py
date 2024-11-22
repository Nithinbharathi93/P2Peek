from pyngrok import ngrok

# Step 1: Authenticate ngrok
ngrok.set_auth_token("2ly0aXUlC9KdEJovwEKz5In1HNz_42Q35noMSzAUHAdm7FUyb")  # Replace with your ngrok auth token

# Step 2: Start an ngrok tunnel for your WSS server
# Assuming your WSS server runs on port 8080
wsLink = input("Enter URL: ")
PORT = wsLink.split(":")[-1]
wss_tunnel = ngrok.connect(PORT, "tcp")

# Get the public URL
ngrok_url = wss_tunnel.public_url
ngrok_wss_url = ngrok_url.replace("tcp://", "wss://")

print(f"Your WSS URL: {ngrok_wss_url}")
