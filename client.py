import socket
import json

HOST = '192.168.0.100'
PORT = 5353

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server")

    # Send message to server
    message = {"message": "server"}
    message_json = json.dumps(message)
    s.sendall(message_json.encode())

    # Receive response from server
    response = s.recv(1024)
    print(f"Received response: {response.decode()}")

print("Disconnected from server")
