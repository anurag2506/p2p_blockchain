# This is a chat application consisting of multiple peers

# Multiple peers can communicate with each other over the TCP network
# Each peer can send and receive messages simultaneously, 
# maintain a list of connected peers, and allow users to query active connections
import socket
import threading
import select

class Peer():
    def __init__(self, name,ip, port):
        self.ip = ip
        self.name = name
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Fix port in use issue

        print(f"Binding to IP: {self.ip}, Port: {self.port}")
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.ip}:{self.port}")
        self.peers = {} 
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        
    def listen_for_messages(self):
        print(f"Server listening on port{self.port}")
        while True:
            readable,_,_ = select.select([self.server_socket],[],[],1)
            
            for sock in readable:
                conn, addr = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args = (conn,addr), daemon=True).start()
                
    
    def handle_client(self,conn,addr):
        ip,port = addr
        
        print(f"Established connection with {ip}:{port}")  
        while True:
            try:
                msg = conn.recv(1024).decode()
                if not msg:
                    break
                print(f"\n[RECIEVED]{ip}:{port}->{msg}")
                
                if msg.strip().lower() == "exit":
                    del self.peers[(ip,port)]
                    print(f"[INFO] Peer {ip}:{port} disconnected")
                    conn.close()
                    return
                
                self.peers[(ip,port)] = msg
            except:
                break
        conn.close()

# Sends a particular message to a particular port and ip
    def send_message(self,target_ip,target_port, message):
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            sock.sendall(message.encode())
            print(f"Send {message} to {target_ip}:{target_port}")
            sock.close()
        except Exception as e:
            print(f"[ERROR] Could not send message: {e}")
    
# Helps you view all the possible peers to connected
    def query_peers(self):
        if self.peers:
            print("Connected Peers:")
        for peer, addr in self.peers.items():
            print(f"{peer}: {addr[0]}:{addr[1]}")
        else:
            print("No connected peers")
            
    
    def menu(self):
        while True:
            print("\n***** Menu *****")
            print("1. Send message")
            print("2. Query connected peers")
            print("0. Quit")
            choice = input("Enter choice: ")

            if choice == "1":
                target_ip = input("Enter recipient’s IP address: ")
                target_port = int(input("Enter recipient’s port number: "))
                message = input("Enter your message: ")
                self.send_message(target_ip, target_port, message)

            elif choice == "2":
                self.query_peers()

            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid choice, try again.")
                
name = input("Enter your name: ")
ip = input("Enter your IP address: ")
port = int(input("Enter your port number: "))

peer = Peer(name,ip,port)
peer.menu()
  
        
        