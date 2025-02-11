import socket
import threading

def receive_messages(server_socket):
    while True:
        try:
            conn, addr = server_socket.accept()
            message = conn.recv(1024).decode()
            print(f"\nReceived from {addr}: {message}")
        except Exception as e:
            print("[Receive Error]:", e)
            break

def send_message():
    while True:
        ip = input("\nEnter recipient's IP (e.g., 127.0.0.1): ").strip()
        port = input("Enter recipient's port: ").strip()

        if not ip or not port.isdigit():
            print("[Error] Invalid IP or Port. Try again.")
            continue

        port = int(port)
        message = input("Enter message: ")

        try:
            print(f"[DEBUG] Connecting to {ip}:{port}...")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))
            client_socket.send(message.encode())
            client_socket.close()
            print("[Success] Message sent.")
        except Exception as e:
            print("[Send Error]:", e)

def start_peer():
    ip = "127.0.0.1"
    port = int(input("Enter your port number: "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)

    print(f"Listening on {ip}:{port}")

    threading.Thread(target=receive_messages, args=(server_socket,), daemon=True).start()

    send_message()

if __name__ == "__main__":
    start_peer()