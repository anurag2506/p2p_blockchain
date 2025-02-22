# This is a chat application consisting of multiple peers

# Multiple peers can communicate with each other over the TCP network
# Each peer can send and receive messages simultaneously, 
# maintain a list of connected peers, and allow users to query active connections
import socket
import threading
import select

class Peer():
    def __init__(self, name, port):
        # self.ip = ip
        self.ip = self.get_local_ip()
        self.name = name
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Fix port in use issue

        print(f"Binding to IP: {self.ip}, Port: {self.port}")
        self.server_socket.bind(("0.0.0.0", self.port)) # ip can be replaced with self.ip if needed
        self.server_socket.listen(5)
        print(f"Server listening on 0.0.0.0 :{self.port}")
        self.peers = {} 
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
    
    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8",80)) # Google DNS server
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip
    def listen_for_messages(self):
        print(f"Server listening on port{self.port}")
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self,conn): 
        while True:
            try:
                msg = conn.recv(1024).decode().strip()
                if msg:
                   parts = msg.split(" ",2) 
                   
                   if len(parts) < 3:
                       print(f"Invalid message format")
                       return
                   sender_info, sender_team, message = parts
                   sender_ip, sender_port = sender_info.split(":")
                   
                    # Store sender in the peers dictionary
                   self.peers[sender_info] = sender_team
                   print(f"✅ Peer added: {sender_info} ({sender_team})")
            except Exception as e:
                print(f"⚠️ Error handling message: {e}")
            finally:
                conn.close()

# Sends a particular message to a particular port and ip
    def send_message(self, target_ip, target_port, message):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            formatted_message = f"{self.ip}:{self.port} {self.team_name} {message}"
            sock.sendall(formatted_message.encode())
            print(f"Sent: {formatted_message} to {target_ip}:{target_port}")
            sock.close()
        except Exception as e:
            print(f"Could not send message to {target_ip}:{target_port} - {e}")
    
# Helps you view all the possible peers to connected
    def query_peers(self):
        if self.peers:
            print("Connected Peers:")
        for peer, team in self.peers.items():
            print(f"{peer}: {(team)}")
        else:
            print("No connected peers")

# Helps u to connect to nodes that have already sent previous messages
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
            print("0. Quit")

            choice = input("Enter choice: ")

            if choice == "1":
                target_ip = input("Enter recipient’s IP: ")
                target_port = int(input("Enter recipient’s port: "))
                message = input("Enter your message: ")
                self.send_message(target_ip, target_port, message)
                
                # Specific 2 ports in which messages are to be sent
                self.send_message("10.206.4.122", 1255, message)
                self.send_message("10.206.5.228", 6555, message)

            elif choice == "2":
                self.query_peers()

            elif choice == "3":
                self.connect_to_active_peers()

            elif choice == "0":
                print(" Exiting...")
                break

            else:
                print(" Invalid choice, try again.")
                
if __name__ == "__main__":
    team_name = input("Enter your team name: ")
    port = int(input("Enter your port number: "))

    peer = Peer(team_name, port)
    peer.menu()
        
        