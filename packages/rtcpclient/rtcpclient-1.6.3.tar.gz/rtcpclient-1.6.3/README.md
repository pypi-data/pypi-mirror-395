# rtcpclient

**rtcpclient** is a simple and powerful Python module for building real-time communication applications. Inspired by the rtcpclient standard, it allows you to handle audio, video, and P2P data with low latency and minimal syntax.

---

## Features

* **P2P Communication**: Direct data exchange between clients without a central server.
* **Audio & Video**: Real-time transmission with low latency.
* **Data Channels**: Send and receive text or JSON messages instantly.
* **Event Handling**: Simple callbacks for `on_connect`, `on_message`, `on_disconnect`.
* **Secure**: Built-in DTLS/SRTP encryption.
* **Interoperable**: Compatible with browsers and other rtcpclient clients.

---

## Installation

```bash
pip install rtcpclient
```



---

## Basic Usage

### Create a client and connect

```python
from rtcpclient import rtcpclientClient

# Initialize the client
client = rtcpclientClient(username="Alice")

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
