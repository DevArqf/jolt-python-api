import pytest
from jolt import JoltResponseParser
from jolt.response import JoltOkResponse, JoltErrorResponse, JoltTopicMessage
from jolt.exceptions import JoltException

def test_parse_valid_json():
    data = JoltResponseParser.parse('{"ok": true}')
    assert data["ok"] is True

def test_parse_invalid_json():
    with pytest.raises(JoltException):
        JoltResponseParser.parse("not valid json")

def test_parse_ok_response():
    response = JoltResponseParser.parse_response('{"ok": true}')
    assert isinstance(response, JoltOkResponse)
    assert response.is_ok() is True

def test_parse_error_response():
    response = JoltResponseParser.parse_response('{"ok": false, "error": "test error"}')
    assert isinstance(response, JoltErrorResponse)
    assert response.is_ok() is False
    assert response.get_error() == "test error"

def test_parse_topic_message():
    response = JoltResponseParser.parse_response('{"topic": "test.topic", "data": "test message"}')
    assert isinstance(response, JoltTopicMessage)
    assert response.get_topic() == "test.topic"
    assert response.get_data() == "test message"

def test_parse_unknown_response():
    with pytest.raises(JoltException):
        JoltResponseParser.parse_response('{"unknown": "format"}')

def test_error_response_string():
    response = JoltErrorResponse({"ok": False, "error": "test error"})
    assert "test error" in str(response)

def test_topic_message_string():
    response = JoltTopicMessage({"topic": "topic", "data": "data"})
    assert "topic" in str(response)
    assert "data" in str(response)

def test_ok_response():
    response = JoltOkResponse({"ok": True})
    assert response.is_ok() is True

def test_response_raw_data():
    raw = {"topic": "test", "data": "message"}
    response = JoltTopicMessage(raw)
    assert response.get_raw() == raw