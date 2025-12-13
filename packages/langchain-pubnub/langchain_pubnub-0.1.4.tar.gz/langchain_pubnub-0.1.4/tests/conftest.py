"""Pytest configuration and shared fixtures for langchain-pubnub tests."""

import os
from unittest.mock import MagicMock

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "requires(requirement): mark test as requiring specific feature"
    )
    config.addinivalue_line("markers", "integration: mark test as an integration test")


@pytest.fixture(scope="session")
def pubnub_publish_key() -> str:
    """Get PubNub publish key from environment or use demo."""
    return os.getenv("PUBNUB_PUBLISH_KEY", "demo")


@pytest.fixture(scope="session")
def pubnub_subscribe_key() -> str:
    """Get PubNub subscribe key from environment or use demo."""
    return os.getenv("PUBNUB_SUBSCRIBE_KEY", "demo")


@pytest.fixture
def mock_pubnub_envelope() -> MagicMock:
    """Create a mock PubNub envelope response."""
    envelope = MagicMock()
    envelope.result.timetoken = 17193163560057793
    envelope.status.is_error.return_value = False
    return envelope


@pytest.fixture
def mock_history_envelope() -> MagicMock:
    """Create a mock PubNub history envelope response."""
    envelope = MagicMock()

    mock_message = MagicMock()
    mock_message.message = {"text": "Test message"}
    mock_message.timetoken = 17193163560057793
    mock_message.meta = None

    envelope.result.channels = {"test-channel": [mock_message]}
    envelope.status.is_error.return_value = False
    return envelope
