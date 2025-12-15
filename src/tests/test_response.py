import pytest
from jolt import JoltResponseParser, JoltErrorResponse, JoltTopicMessage
from jolt.exceptions import JoltException

def test_parse_valid_json():
    data = JoltResponseParser.parse('{"ok": true}')
    assert data["ok"] is True

def test_parse_invalid_json():
    with pytest.raises(JoltException):
        JoltResponseParser.parse("not valid json")

def test_parse_error_response():
    data = {"error": "authentication failed"}
    error = JoltResponseParser.parse_error_response(data)
    
    assert isinstance(error, JoltErrorResponse)
    assert error.get_error() == "authentication failed"

def test_parse_error_response_missing_field():
    data = {}
    error = JoltResponseParser.parse_error_response(data)
    
    assert error.get_error() == "Unknown error"

def test_parse_topic_message():
    data = {"topic": "test.topic", "data": "test message"}
    msg = JoltResponseParser.parse_topic_message(data)
    
    assert isinstance(msg, JoltTopicMessage)
    assert msg.get_topic() == "test.topic"
    assert msg.get_data() == "test message"

def test_parse_topic_message_missing_fields():
    data = {}
    msg = JoltResponseParser.parse_topic_message(data)
    
    assert msg.get_topic() == ""
    assert msg.get_data() == ""

def test_error_response_string():
    error = JoltErrorResponse("test error")
    assert "test error" in str(error)

def test_topic_message_string():
    msg = JoltTopicMessage("topic", "data")
    assert "topic" in str(msg)
    assert "data" in str(msg)