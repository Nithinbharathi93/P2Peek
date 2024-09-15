# import ngrok python sdk
import ngrok
import time

# Establish connectivity

token = "2ly0aXUlC9KdEJovwEKz5In1HNz_42Q35noMSzAUHAdm7FUyb"
ngrok.set_auth_token(token)
listener = ngrok.forward(56025, authtoken_from_env=True)

# Output ngrok url to console
print(f"Ingress established at {listener.url()}")

# Keep the listener alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing listener")