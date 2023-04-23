import socket
import threading
import json

def handle_client(conn, addr):
    print(f"Connected by {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            print(f"Client {addr} disconnected")
            break

        print(f"Received data: {data.decode()}")

        # Process received data
        try:
            data_json = json.loads(data.decode())
            if "pos_x" in data_json and "pos_y" in data_json:
                pos_x = data_json["pos_x"]
                pos_y = data_json["pos_y"]
                print(f"Player position: ({pos_x}, {pos_y})")
                response = {"message": "Position saved"}
            else:
                response = {"error": "Invalid message format"}
        except json.JSONDecodeError:
            response = {"error": "Invalid JSON format"}

        # Send response
        response_json = json.dumps(response)
        conn.sendall(response_json.encode())

    conn.close()

def server(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
