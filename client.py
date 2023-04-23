import socket
import json
import time

HOST = '192.168.0.100'
PORT = 5353

def send_player_position(s, pos_x, pos_y):
    # Send message to server
    message = {"message": "player_position", "pos_y":pos_y, "pos_x":pos_x}

    message_json = json.dumps(message)
    s.sendall(message_json.encode())

    # Receive response from server
    response = s.recv(1024)
    print(f"Received response: {response.decode()}")

def client(HOST, PORT, pos_x, pos_y):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to server")

        while True:
            send_player_position(s, pos_x, pos_y)
            time.sleep(0.05)

    print("Disconnected from server")
