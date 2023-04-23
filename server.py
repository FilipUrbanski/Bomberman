import socket

HOST = '42.0.144.90'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    data = conn.recv(1024)
    print(f"Received data: {data.decode()}")
    conn.sendall(b"Hello, client!")
    conn.close()
