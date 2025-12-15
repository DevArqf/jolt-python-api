import pytest
from jolt import JoltConfig, JoltConfigBuilder

def test_config_default_values():
    config = JoltConfig()
    assert config.get_host() == "127.0.0.1"
    assert config.get_port() == 8080

def test_config_custom_values():
    config = JoltConfig(host="192.168.1.100", port=9999)
    assert config.get_host() == "192.168.1.100"
    assert config.get_port() == 9999

def test_config_builder():
    config = JoltConfig.new_builder() \
        .host("localhost") \
        .port(7777) \
        .build()
    
    assert config.get_host() == "localhost"
    assert config.get_port() == 7777

def test_config_builder_defaults():
    config = JoltConfig.new_builder().build()
    assert config.get_host() == "127.0.0.1"
    assert config.get_port() == 8080

def test_config_string_representation():
    config = JoltConfig("test.host", 1234)
    assert "test.host" in str(config)
    assert "1234" in str(config)