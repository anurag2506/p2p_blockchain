# This is a chat application consisting of multiple peers

# Multiple peers can communicate with each other over the TCP network
# Each peer can send and receive messages simultaneously, 
# maintain a list of connected peers, and allow users to query active connections
import socket
import threading

class Peer():
    def __init__(self,port,ip):
        self.port = port
        self.ip = ip
        self.peers = {} # Stores the last ip and port for the most recent message
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5) # max 5 unacepted connection requests can wait in the chat room
        
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        
    def listen_for_messages(self):
        
        while True:
            
        