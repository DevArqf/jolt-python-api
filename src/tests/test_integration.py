import pytest
import time
import threading
from typing import Optional
from jolt import JoltClient, JoltConfig, JoltMessageHandler
from jolt import JoltErrorResponse, JoltTopicMessage

JOLT_HOST = "127.0.0.1"
JOLT_PORT = 8080

class TestMessageHandler(JoltMessageHandler):
    
    def __init__(self):
        self.ok_responses = []
        self.errors = []
        self.messages = []
        self.disconnected_event = None
        self.lock = threading.Lock()
    
    def on_ok(self, raw_line: str):
        with self.lock:
            self.ok_responses.append(raw_line)
    
    def on_error(self, error: JoltErrorResponse, raw_line: str):
        with self.lock:
            self.errors.append(error)
    
    def on_topic_message(self, msg: JoltTopicMessage, raw_line: str):
        with self.lock:
            self.messages.append(msg)
    
    def on_disconnected(self, cause: Optional[Exception]):
        with self.lock:
            self.disconnected_event = cause
    
    def wait_for_messages(self, count: int, timeout: float = 5.0):
        start = time.time()
        while time.time() - start < timeout:
            with self.lock:
                if len(self.messages) >= count:
                    return True
            time.sleep(0.1)
        return False

@pytest.fixture
def config():
    return JoltConfig.new_builder() \
        .host(JOLT_HOST) \
        .port(JOLT_PORT) \
        .build()

@pytest.fixture
def client(config):
    handler = TestMessageHandler()
    client = JoltClient(config, handler)
    client.connect()
    yield client, handler
    client.close()

def test_connect_disconnect(config):
    handler = TestMessageHandler()
    client = JoltClient(config, handler)
    
    client.connect()
    assert client.is_connected()
    
    client.close()
    time.sleep(0.5)
    assert not client.is_connected()

def test_ping(client):
    client_obj, handler = client
    
    client_obj.ping()
    time.sleep(0.5)
    
    assert len(handler.ok_responses) > 0

def test_single_topic_pubsub(client):
    client_obj, handler = client
    
    topic = "test.single"
    message = "test message"
    
    client_obj.subscribe(topic)
    time.sleep(0.5)
    
    client_obj.publish(topic, message)
    
    assert handler.wait_for_messages(1)
    
    received = handler.messages[0]
    assert received.get_topic() == topic
    assert received.get_data() == message

def test_multiple_topics(client):
    client_obj, handler = client
    
    topics = ["topic1", "topic2", "topic3"]
    
    for topic in topics:
        client_obj.subscribe(topic)
    time.sleep(0.5)
    
    for i, topic in enumerate(topics):
        client_obj.publish(topic, f"message {i}")
    
    assert handler.wait_for_messages(len(topics))
    
    received_topics = [msg.get_topic() for msg in handler.messages]
    for topic in topics:
        assert topic in received_topics

def test_unsubscribe(client):
    client_obj, handler = client
    
    topic = "test.unsub"
    
    client_obj.subscribe(topic)
    time.sleep(0.5)
    client_obj.publish(topic, "message 1")
    assert handler.wait_for_messages(1)
    
    count_after_sub = len(handler.messages)
    
    client_obj.unsubscribe(topic)
    time.sleep(0.5)
    
    client_obj.publish(topic, "message 2")
    time.sleep(0.5)
    
    assert len(handler.messages) == count_after_sub

def test_multiple_clients():
    config = JoltConfig.new_builder() \
        .host(JOLT_HOST) \
        .port(JOLT_PORT) \
        .build()
    
    handler1 = TestMessageHandler()
    client1 = JoltClient(config, handler1)
    client1.connect()
    
    handler2 = TestMessageHandler()
    client2 = JoltClient(config, handler2)
    client2.connect()
    
    try:
        topic = "test.multi"
        
        client1.subscribe(topic)
        client2.subscribe(topic)
        time.sleep(0.5)
        
        client1.publish(topic, "from client1")
        
        assert handler1.wait_for_messages(1)
        assert handler2.wait_for_messages(1)
        
        assert handler1.messages[0].get_data() == "from client1"
        assert handler2.messages[0].get_data() == "from client1"
    
    finally:
        client1.close()
        client2.close()

def test_high_volume():
    config = JoltConfig.new_builder() \
        .host(JOLT_HOST) \
        .port(JOLT_PORT) \
        .build()
    
    handler = TestMessageHandler()
    client = JoltClient(config, handler)
    client.connect()
    
    try:
        topic = "test.volume"
        message_count = 100
        
        client.subscribe(topic)
        time.sleep(0.5)
        
        for i in range(message_count):
            client.publish(topic, f"message {i}")
        
        assert handler.wait_for_messages(message_count, timeout=10.0)
        
        assert len(handler.messages) >= message_count
    
    finally:
        client.close()