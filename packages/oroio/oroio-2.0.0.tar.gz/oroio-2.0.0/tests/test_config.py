"""Tests for configuration management"""

import pytest
from pathlib import Path
import json
import tempfile
import os


def test_config_initialization():
    """Test config directory creation"""
    from oroio.config import Config
    
    # Create temporary config directory
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config()
        # Default config should exist
        assert config.config_dir.exists()


def test_config_load_default():
    """Test loading default configuration"""
    from oroio.config import Config
    
    config = Config()
    data = config.load()
    
    assert 'api_endpoint' in data
    assert 'access_token' in data
    assert 'refresh_token' in data


def test_config_set_endpoint():
    """Test setting API endpoint"""
    from oroio.config import Config
    
    config = Config()
    test_url = "https://api.test.com"
    config.set_api_endpoint(test_url)
    
    assert config.get_api_endpoint() == test_url


def test_config_tokens():
    """Test token management"""
    from oroio.config import Config
    
    config = Config()
    
    # Set tokens
    access = "test_access_token"
    refresh = "test_refresh_token"
    config.set_tokens(access, refresh)
    
    assert config.get_access_token() == access
    assert config.is_authenticated() is True
    
    # Clear tokens
    config.clear_tokens()
    assert config.get_access_token() is None
    assert config.is_authenticated() is False


def test_config_env_override():
    """Test environment variable override"""
    from oroio.config import Config
    
    # Set environment variable
    test_endpoint = "https://env-test.com"
    os.environ["OROIO_API_ENDPOINT"] = test_endpoint
    
    try:
        config = Config()
        assert config.get_api_endpoint() == test_endpoint
    finally:
        # Cleanup
        del os.environ["OROIO_API_ENDPOINT"]
