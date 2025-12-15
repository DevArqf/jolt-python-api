import time
from jolt import JoltClient, JoltConfig, JoltMessageHandler
from jolt import JoltErrorResponse, JoltTopicMessage
from typing import Optional

class SimpleChatHandler(JoltMessageHandler):
    
    def on_ok(self, raw_line: str):
        print(f"✓ OK")
    
    def on_error(self, error: JoltErrorResponse, raw_line: str):
        print(f"✗ Error: {error.get_error()}")
    
    def on_topic_message(self, msg: JoltTopicMessage, raw_line: str):
        print(f"📩 [{msg.get_topic()}] {msg.get_data()}")
    
    def on_disconnected(self, cause: Optional[Exception]):
        if cause:
            print(f"⚠ Disconnected: {cause}")
        else:
            print("👋 Connection closed")


def main():
    config = JoltConfig.new_builder() \
        .host("127.0.0.1") \
        .port(8080) \
        .build()
    
    handler = SimpleChatHandler()
    client = JoltClient(config, handler)
    
    try:
        print("🔌 Connecting to Jolt server...")
        client.connect()
        print("✓ Connected!\n")
        
        # Authenticate (uncomment if your server requires it)
        # client.auth("username", "password")
        
        print("📡 Subscribing to chat.room1...")
        client.subscribe("chat.room1")
        
        print("\n📤 Publishing messages...")
        client.publish("chat.room1", "Hello from Python!")
        client.publish("chat.room1", "This is a test message")
        
        print("\n🏓 Sending ping...")
        client.ping()
        
        print("\n📡 Listening for messages (press Ctrl+C to exit)...\n")
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        client.close()
        print("✓ Disconnected")


if __name__ == "__main__":
    main()