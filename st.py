import socket
import threading
import streamlit as st

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

class Peer:
    def __init__(self, name,ip,port):
        self.ip = ip
        self.name = name
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        self.peers = {}  # Dictionary to store peer info

        # Start listening for messages in a separate thread
        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def listen_for_messages(self):
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
                    break

                sender_info, sender_team, message = parts
                sender_ip, sender_port = sender_info.split(":")
                self.peers[sender_info] = sender_team  

                # Add received message to chat history
                st.session_state.messages.append(f"📩 From {sender_team} ({sender_ip}:{sender_port}): {message}")

        except Exception as e:
            st.session_state.messages.append(f"⚠️ Error handling message: {e}")
        finally:
            conn.close()

    def send_message(self, target_ip, target_port, message):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            formatted_message = f"{self.ip}:{self.port} {self.name} {message}"
            sock.sendall(formatted_message.encode())
            sock.close()

            # Add sent message to chat history
            st.session_state.messages.append(f"📤 To {target_ip}:{target_port}: {message}")

        except Exception as e:
            st.session_state.messages.append(f"⚠️ Could not send message to {target_ip}:{target_port} - {e}")

# Streamlit UI
st.title("🖥️ Peer-to-Peer Messaging")

# Get team name and port
team_name = st.text_input("Enter your team name:", value="TeamA")
port = st.number_input("Enter your port number:", min_value=1024, max_value=65535, value=3000)

if st.button("Start Peer"):
    peer = Peer(team_name, port)
    st.success(f"✅ Peer started at 127.0.0.1:{port}")

# Chat box
st.subheader("📬 Chat Messages")
chat_area = st.empty()

# Display message history
if st.session_state.messages:
    chat_area.markdown("\n".join(st.session_state.messages))

# Send message UI
st.subheader("📤 Send a Message")
target_ip = st.text_input("Recipient's IP", value="127.0.0.1")
target_port = st.number_input("Recipient's Port", min_value=1024, max_value=65535, value=3001)
message = st.text_input("Enter your message")

if st.button("Send Message"):
    if "peer" in locals():
        peer.send_message(target_ip, target_port, message)
        st.experimental_rerun()
    else:
        st.warning("⚠️ Please start the peer first!")