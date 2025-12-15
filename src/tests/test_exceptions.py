import pytest
from jolt.exceptions import JoltException

def test_jolt_exception_creation():
    exc = JoltException("test error")
    assert str(exc) == "test error"

def test_jolt_exception_raise():
    with pytest.raises(JoltException) as exc_info:
        raise JoltException("test error")
    
    assert "test error" in str(exc_info.value)

def test_jolt_exception_inheritance():
    assert issubclass(JoltException, Exception)