<h1><b>Peer to Peer Connection System</b></h1>
<h3> Overview of the project: </h3>
<p> This repo consists of a system that helps in peer-peer communication without any packet loss. This happens with the help of TCP (Transmission Control Protocol). <br>
TCP is better than UDP when it comes to:<br>
1. No packet loss (No information loss)
2. Sequence of messages that are sent from one peer to another is maintained in this.
3. There might be a bit of latency as compared to UDP, but the tradeoff is good.</p><br>

<h2> About the Repo:</h2>
<p> The <b>peer.py</b> has the testing of a single peer communication with my computer. (Just for testing and understanding)<br>
The <b>chat.py</b> has the implementation of the multi-peer system that can wokr with multiple IP addresses at the same time<br>
The functionalities added to the P2P network:<br>
1. Send a message from your IP to any other IP<br>
2. See the list of active peers right now who have sent messages to you in the past and send them a greeting automatically if their server is running.
3. See the list of peers (active/inactive) to whom you have connected in the past<br>
4. Send messages to the 2 public IPs provided in the assignment<br>
5. Stopping the server</p><br>

<h2>Logic for my IP address:</h2>
<p>We have also provided logic for fetching any system's IP address locally from the DNS server of google so that you don't have to enter your IP manually.</p>
