import socket
import threading

class Peer():
    def __init__(self, name, ip,port):
        # self.ip = self.get_local_ip()
        self.ip = ip
        self.name = name
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print(f"Binding to IP: {self.ip}, Port: {self.port}")
        self.server_socket.bind((self.ip, self.port))  # Use self.ip instead of 0.0.0.0
        self.server_socket.listen(5)
        print(f"Server listening on {self.ip}:{self.port}")
        self.peers = {} 
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
    
    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def listen_for_messages(self):
        print(f"Listening for messages on port {self.port}...")
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn): 
        try:
            while True:
                msg = conn.recv(1024).decode().strip()
                if not msg:
                    break  

                parts = msg.split(" ", 2)
                if len(parts) < 3:
                    print("Invalid message format")
                    break 

                sender_info, sender_team, message = parts
                sender_ip, sender_port = sender_info.split(":")
                self.peers[sender_info] = sender_team  
                print(f" Message from {sender_ip}:{sender_port} ({sender_team}): {message}")

        except ConnectionResetError:
            print("Connection was reset by the peer")
        except Exception as e:
            print(f"⚠️ Error handling message: {e}")
        finally:
            conn.close()  # Ensure the socket is closed properly

    def send_message(self, target_ip, target_port, message):
        try:
            print(f"Attempting to send message to {target_ip}:{target_port}...")  # Debugging
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            formatted_message = f"{self.ip}:{self.port} {self.name} {message}"
            print(f"Formatted Message: {formatted_message}")  # Debugging
            sock.sendall(formatted_message.encode())
            print(f"Sent message to {target_ip}:{target_port}")
            sock.close()
        except Exception as e:
            print(f"Could not send message to {target_ip}:{target_port} - {e}")

    def query_peers(self):
        if self.peers:
            print("Connected Peers:")
            for peer, info in self.peers.items():
                print(f"{peer} - Team: {info['team']}, Last Msg: '{info['last_msg']}'")
        else:
            print("No connected peers")

    def connect_to_active_peers(self):
        for peer in self.peers.keys():
            ip, port = peer.split(":")
            self.send_message(ip, int(port), "Hello again!")

    def menu(self):
        while True:
            print("\n***** Menu *****")
            print("1. Send message")
            print("2. Query connected peers")
            print("3. Connect to active peers")
            print("4. Send message to 10.206.4.122:1255")
            print("5. Send message to 10.206.5.228:6555")
            print("0. Quit")

            choice = input("Enter choice: ")

            if choice == "1":
                target_ip = input("Enter recipient’s IP: ")
                target_port = int(input("Enter recipient’s port: "))
                message = input("Enter your message: ")
                if target_ip == "0.0.0.0":
                    print("Invalid IP address. Use an actual local IP.")
                    continue
                self.send_message(target_ip, target_port, message)

            elif choice == "2":
                self.query_peers()

            elif choice == "3":
                self.connect_to_active_peers()

            elif choice == "4":
                message = input("Enter your message: ")
                self.send_message("10.206.4.122", 1255, message)

            elif choice == "5":
                message = input("Enter your message: ")
                self.send_message("10.206.5.228", 6555, message)

            elif choice == "0":
                print("Exiting...")
                break

            else:
                print("Invalid choice, try again.")

if __name__ == "__main__":
    team_name = input("Enter your team name: ")
    ip = input("Enter your IP: ")
    port = int(input("Enter your port number: "))
    peer = Peer(team_name,ip, port)
    peer.menu()