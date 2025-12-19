import json
import pytest
from jolt import JoltRequestBuilder

def test_auth_request():
    request = JoltRequestBuilder.auth("testuser", "testpass")
    data = json.loads(request)
    
    assert data["cmd"] == "auth"
    assert data["user"] == "testuser"
    assert data["pass"] == "testpass"

def test_subscribe_request():
    request = JoltRequestBuilder.subscribe("test.topic")
    data = json.loads(request)
    
    assert data["cmd"] == "sub"
    assert data["topic"] == "test.topic"

def test_unsubscribe_request():
    request = JoltRequestBuilder.unsubscribe("test.topic")
    data = json.loads(request)
    
    assert data["cmd"] == "unsub"
    assert data["topic"] == "test.topic"

def test_publish_request():
    request = JoltRequestBuilder.publish("test.topic", "test message")
    data = json.loads(request)
    
    assert data["cmd"] == "pub"
    assert data["topic"] == "test.topic"
    assert data["data"] == "test message"

def test_ping_request():
    request = JoltRequestBuilder.ping()
    data = json.loads(request)
    
    assert data["cmd"] == "ping"

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
        assert "cmd" in data

def test_requests_end_with_newline():
    """Verify all requests end with newline for NDJSON protocol"""
    requests = [
        JoltRequestBuilder.auth("user", "pass"),
        JoltRequestBuilder.subscribe("topic"),
        JoltRequestBuilder.unsubscribe("topic"),
        JoltRequestBuilder.publish("topic", "data"),
        JoltRequestBuilder.ping()
    ]
    
    for request in requests:
        assert request.endswith('\n'), f"Request should end with newline: {request}"