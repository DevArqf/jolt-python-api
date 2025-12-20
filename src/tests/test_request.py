import json
import pytest
from jolt import JoltRequestBuilder

def test_auth_request():
    request = JoltRequestBuilder.auth("testuser", "testpass")
    data = json.loads(request)
    
    assert data["op"] == "auth"
    assert data["user"] == "testuser"
    assert data["pass"] == "testpass"

def test_subscribe_request():
    request = JoltRequestBuilder.subscribe("test.topic")
    data = json.loads(request)
    
    assert data["op"] == "sub"
    assert data["topic"] == "test.topic"

def test_unsubscribe_request():
    request = JoltRequestBuilder.unsubscribe("test.topic")
    data = json.loads(request)
    
    assert data["op"] == "unsub"
    assert data["topic"] == "test.topic"

def test_publish_request():
    request = JoltRequestBuilder.publish("test.topic", "test message")
    data = json.loads(request)
    
    assert data["op"] == "pub"
    assert data["topic"] == "test.topic"
    assert data["data"] == "test message"

def test_ping_request():
    request = JoltRequestBuilder.ping()
    data = json.loads(request)
    
    assert data["op"] == "ping"

def test_request_is_valid_json():
    requests = [
        JoltRequestBuilder.auth("user", "pass"),
        JoltRequestBuilder.subscribe("topic"),
        JoltRequestBuilder.unsubscribe("topic"),
        JoltRequestBuilder.publish("topic", "data"),
        JoltRequestBuilder.ping()
    ]
    
    for request in requests:
        data = json.loads(request)
        assert "op" in data

def test_requests_end_with_newline():
    requests = [
        JoltRequestBuilder.auth("user", "pass"),
        JoltRequestBuilder.subscribe("topic"),
        JoltRequestBuilder.unsubscribe("topic"),
        JoltRequestBuilder.publish("topic", "data"),
        JoltRequestBuilder.ping()
    ]
    
    for request in requests:
        assert request.endswith('\n'), f"Request should end with newline: {request}"

def test_command_formats():
    auth_req = json.loads(JoltRequestBuilder.auth("u", "p"))
    assert auth_req["op"] == "auth"
    
    sub_req = json.loads(JoltRequestBuilder.subscribe("t"))
    assert sub_req["op"] == "sub"
    
    unsub_req = json.loads(JoltRequestBuilder.unsubscribe("t"))
    assert unsub_req["op"] == "unsub"
    
    pub_req = json.loads(JoltRequestBuilder.publish("t", "d"))
    assert pub_req["op"] == "pub"
    
    ping_req = json.loads(JoltRequestBuilder.ping())
    assert ping_req["op"] == "ping"