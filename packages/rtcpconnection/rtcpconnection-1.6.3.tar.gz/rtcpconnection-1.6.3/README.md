# rtcpconnection

**rtcpconnection** is a simple and powerful Python module for building real-time communication applications. Inspired by the rtcpconnection standard, it allows you to handle audio, video, and P2P data with low latency and minimal syntax.

---

## Features

* **P2P Communication**: Direct data exchange between clients without a central server.
* **Audio & Video**: Real-time transmission with low latency.
* **Data Channels**: Send and receive text or JSON messages instantly.
* **Event Handling**: Simple callbacks for `on_connect`, `on_message`, `on_disconnect`.
* **Secure**: Built-in DTLS/SRTP encryption.
* **Interoperable**: Compatible with browsers and other rtcpconnection clients.

---

## Installation

```bash
pip install rtcpconnection
```



---

## Basic Usage

### Create a client and connect

```python
from rtcpconnection import rtcpconnectionClient

# Initialize the client
client = rtcpconnectionClient(username="Alice")

# Event triggered when a message is received
@client.on("message")
def handle_message(sender, content):
    print(f"{sender} says: {content}")

# Connect to a peer
client.connect("bob_peer_id")

# Send a message
client.send("bob_peer_id", "Hi Bob!")

# Listen for events
client.listen()
```

### Audio/Video example

```python
client.connect_audio()
client.connect_video()
```

---

## Use Cases

* Real-time audio and video chats
* P2P multiplayer games
* Streaming and data sharing
* Collaborative tools (drawing, shared documents)

---
