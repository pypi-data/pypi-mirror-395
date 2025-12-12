"""Pytest configuration and fixtures for VPN Monitor tests.

This module provides common fixtures and configuration for the test suite.
"""

import pytest


@pytest.fixture
def sample_ip():
    """Provide a sample IP address for testing."""
    return "192.168.1.1"


@pytest.fixture
def sample_country_code():
    """Provide a sample country code for testing."""
    return "HU"


@pytest.fixture
def allowed_ips_content():
    """Provide sample allowed IPs file content."""
    return """# Allowed IPs for VPN bypass
203.0.113.1
198.51.100.2
# Another comment
10.0.0.1
"""


@pytest.fixture
def mock_process_list():
    """Provide a mock list of process names."""
    return [
        "explorer.exe",
        "msrdc.exe",
        "chrome.exe",
        "Windows365.exe",
    ]


# Add more fixtures as needed for actual tests
