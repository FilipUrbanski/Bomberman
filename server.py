import socket
import threading

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    data = conn.recv(1024)
    print(f"Received data: {data.decode()}")
    conn.sendall(b"Hello, client!")
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