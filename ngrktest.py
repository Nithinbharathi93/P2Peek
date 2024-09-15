import socket 
from _thread import *
import sys
from collections import defaultdict as df
import ngrok
import time

class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class Server:
    def __init__(self):
        self.rooms = df(list)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def accept_connections(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.server.bind((self.ip_address, int(self.port)))
        self.server.listen(100)

        while True:
            try:
                connection, address = self.server.accept()
                print(str(address[0]) + ":" + str(address[1]) + " Connected")
                start_new_thread(self.clientThread, (connection,))
            except:
                self.server.close()
                break

    
    def clientThread(self, connection):
        user_id = connection.recv(1024).decode().replace("User ", "")
        room_id = connection.recv(1024).decode().replace("Join ", "")

        if room_id not in self.rooms:
            connection.send("New Group created".encode())
        else:
            connection.send("Welcome to chat room".encode())

        self.rooms[room_id].append(connection)
        print("connection added to the room")

        while True:
            try:
                message = connection.recv(1024)
                if message:
                    print("The message :",str(message.decode()))
                    if str(message.decode()) == "FILE":
                        self.broadcastFile(connection, room_id, user_id)

                    else:
                        message_to_send = "<" + str(user_id) + "> " + message.decode()
                        self.broadcast(message_to_send, connection, room_id)

                else:
                    self.remove(connection, room_id)
            except Exception as e:
                print("Exception arised while recieving message",repr(e))
                print("Client disconnected earlier")
                # exit()
                break
    
    
    def broadcastFile(self, connection, room_id, user_id):
        file_name = connection.recv(1024).decode()
        lenOfFile = connection.recv(1024).decode()
        for client in self.rooms[room_id]:
            if client != connection:
                try: 
                    client.send("FILE".encode())
                    time.sleep(0.1)
                    client.send(file_name.encode())
                    time.sleep(0.1)
                    client.send(lenOfFile.encode())
                    time.sleep(0.1)
                    client.send(user_id.encode())
                except:
                    client.close()
                    self.remove(client, room_id)

        total = 0
        print(file_name, lenOfFile)
        while str(total) != lenOfFile:
            data = connection.recv(1024)
            total = total + len(data)
            for client in self.rooms[room_id]:
                if client != connection:
                    try: 
                        client.send(data)
                        # time.sleep(0.1)
                    except:
                        client.close()
                        self.remove(client, room_id)
        print("Sent")



    def broadcast(self, message_to_send, connection, room_id):
        for client in self.rooms[room_id]:
            if client != connection:
                try:
                    client.send(message_to_send.encode())
                except:
                    client.close()
                    self.remove(client, room_id)

    
    def remove(self, connection, room_id):
        if connection in self.rooms[room_id]:
            self.rooms[room_id].remove(connection)


if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = (s.getsockname()[0])
    print(ip_address)
    l = [(255-int(i))/10 for i in ip_address.split('.')]
    d = {i:j for i, j in enumerate("abcdefghijklmnopqrstuvwxyz")}
    enc = "".join([d[int(i)] for i in l])
    rest = "".join([d[int(str(i)[-1])] for i in l])
    code = "".join([i+j for i, j in zip(enc,rest)])
    print(code)
    s.close()
    s = Server()
    token = "2ly0aXUlC9KdEJovwEKz5In1HNz_42Q35noMSzAUHAdm7FUyb"
    ngrok.set_auth_token(token)
    listener = ngrok.forward(12345, authtoken_from_env=True)
    print(f"Ingress established at {listener.url()}")
    s.accept_connections(ip_address, port)
    