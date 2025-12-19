<div align="center">
<img width="1920" height="1071" alt="image" src="https://github.com/DevArqf/jolt-python-api/blob/f92d146c11c3afa7844d4384f1abbdb3bc99d34c/Jolt%20Logo.png?raw=true" alt="./Jolt Logo.png"/>
</div>

---

A fast, lightweight Python client for the [Jolt](https://github.com/Jolt-Database/Jolt) in-memory messaging broker.

## Features

✅ Native Jolt broker protocol support  
✅ Thread-safe message sending  
✅ Background message receiving  
✅ Simple pub/sub messaging  
✅ No external dependencies (standard library only)  

## Protocol

The Jolt broker uses NDJSON (newline-delimited JSON) over TCP:

### Commands (Client → Broker)
```json
{"cmd": "auth", "user": "username", "pass": "password"}
{"cmd": "sub", "topic": "channel.name"}
{"cmd": "unsub", "topic": "channel.name"}
{"cmd": "pub", "topic": "channel.name", "data": "message"}
{"cmd": "ping"}
```

### Responses (Broker → Client)
```json
{"ok": true}
{"ok": false, "error": "error_message"}
{"topic": "channel.name", "data": "message"}
```

## Installation

```bash
# From source
git clone https://github.com/DevArqf/jolt-python-api.git
cd jolt-python-api
pip install -e .
```

## Quick Start

```python
from jolt import JoltClient, JoltConfig, JoltMessageHandler
from jolt.response import JoltErrorResponse, JoltTopicMessage
from typing import Optional
import time

# 1. Create handler
class MyHandler(JoltMessageHandler):
    def on_ok(self, raw_line: str):
        print("✓ OK")
    
    def on_error(self, error: JoltErrorResponse, raw_line: str):
        print(f"✗ Error: {error.get_error()}")
    
    def on_topic_message(self, msg: JoltTopicMessage, raw_line: str):
        print(f"📩 [{msg.get_topic()}] {msg.get_data()}")
    
    def on_disconnected(self, cause: Optional[Exception]):
        print(f"👋 Disconnected: {cause if cause else 'clean shutdown'}")

# 2. Configure and connect
config = JoltConfig.new_builder() \
    .host("127.0.0.1") \
    .port(8080) \
    .build()

handler = MyHandler()
client = JoltClient(config, handler)
client.connect()

# 3. Use the client
client.subscribe("chat.general")
client.publish("chat.general", "Hello, Jolt!")
client.ping()

time.sleep(1)
client.close()
```

## API Reference

### JoltClient

Main client for interacting with the Jolt broker.

```python
client = JoltClient(config, handler)

# Connection
client.connect()
client.close()
client.is_connected() -> bool

# Operations
client.auth(username, password)
client.subscribe(topic)
client.unsubscribe(topic)
client.publish(topic, data)
client.ping()
```

### JoltMessageHandler

Abstract handler for broker messages. Implement all methods:

```python
class MyHandler(JoltMessageHandler):
    def on_ok(self, raw_line: str):
        """Called when broker sends {"ok": true}"""
        pass
    
    def on_error(self, error: JoltErrorResponse, raw_line: str):
        """Called when broker sends {"ok": false, "error": "..."}"""
        pass
    
    def on_topic_message(self, msg: JoltTopicMessage, raw_line: str):
        """Called when receiving a message on subscribed topic"""
        pass
    
    def on_disconnected(self, cause: Optional[Exception]):
        """Called when connection is lost"""
        pass
```

### Response Objects

```python
# JoltOkResponse
response.is_ok() -> bool

# JoltErrorResponse
error.get_error() -> str
error.is_ok() -> bool  # Always False

# JoltTopicMessage
message.get_topic() -> str
message.get_data() -> str
```

## Examples

### Simple Chat

```python
import time
from jolt import JoltClient, JoltConfig, JoltMessageHandler
from jolt.response import JoltErrorResponse, JoltTopicMessage
from typing import Optional

class ChatHandler(JoltMessageHandler):
    def on_ok(self, raw_line: str):
        pass  # Silent
    
    def on_error(self, error: JoltErrorResponse, raw_line: str):
        print(f"Error: {error.get_error()}")
    
    def on_topic_message(self, msg: JoltTopicMessage, raw_line: str):
        print(f"[{msg.get_topic()}] {msg.get_data()}")
    
    def on_disconnected(self, cause: Optional[Exception]):
        print("Disconnected")

# Setup
config = JoltConfig.new_builder().host("127.0.0.1").port(8080).build()
client = JoltClient(config, ChatHandler())
client.connect()

# Subscribe and chat
client.subscribe("chat.room1")
client.publish("chat.room1", "Hello everyone!")

# Keep alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.close()
```

### Multiple Topics

```python
topics = ["news", "sports", "weather"]

# Subscribe to all
for topic in topics:
    client.subscribe(topic)

# Publish to each
client.publish("news", "Breaking: Python API released!")
client.publish("sports", "Score: 3-2")
client.publish("weather", "Sunny, 25°C")
```

### Error Handling

```python
class RobustHandler(JoltMessageHandler):
    def on_error(self, error: JoltErrorResponse, raw_line: str):
        error_msg = error.get_error()
        
        if "auth" in error_msg.lower():
            print("Authentication failed!")
        elif "unknown_topic" in error_msg:
            print("Topic doesn't exist!")
        else:
            print(f"Error: {error_msg}")
    
    def on_disconnected(self, cause: Optional[Exception]):
        if cause:
            print(f"Connection lost: {cause}")
            # Implement reconnection logic here
```

## Testing

```bash
# Run unit tests (no broker required)
pytest src/tests/test_config.py -v
pytest src/tests/test_request.py -v
pytest src/tests/test_response.py -v

# Run all tests
pytest src/tests/ -v
```

## Running the Jolt Broker

You need the actual Jolt broker to use this client:

```bash
# Get the broker
git clone https://github.com/Jolt-Database/Jolt.git
cd Jolt

# Build (requires Go)
go build -o jolt-broker

# Run
./jolt-broker -port 8080
```

## Protocol Differences from Java API

This Python API is designed to work with the **actual Jolt broker**, not the jolt-java-api. Key differences:

| Feature | This API | Java API Assumption |
|---------|----------|---------------------|
| Command key | `"cmd"` | `"op"` |
| Subscribe | `"sub"` | `"subscribe"` |
| Unsubscribe | `"unsub"` | `"unsubscribe"` |
| Publish | `"pub"` | `"publish"` |

This implementation has been tested against the actual Jolt broker and follows its protocol exactly.

## Troubleshooting

### Connection Refused
- Ensure broker is running: `./jolt-broker -port 8080`
- Check host and port in config
- Verify no firewall blocking port 8080

### No Messages Received
- Ensure you're subscribed before publishing
- Check handler's `on_topic_message` is implemented
- Verify broker is relaying messages (check broker logs)

### Authentication Errors
- Check if broker requires authentication
- Verify username/password are correct
- Call `client.auth()` before other operations

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

Created for use with the [Jolt Database](https://github.com/Jolt-Database/Jolt) project.