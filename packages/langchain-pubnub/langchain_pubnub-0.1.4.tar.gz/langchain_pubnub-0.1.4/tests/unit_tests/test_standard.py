"""Standard LangChain tests for PubNub tools.

These tests use the langchain-tests package to verify tools conform
to LangChain's standard tool interface.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

try:
    from langchain_tests.unit_tests import ToolsUnitTests

    LANGCHAIN_TESTS_AVAILABLE = True
except ImportError:
    LANGCHAIN_TESTS_AVAILABLE = False
    ToolsUnitTests = object  # type: ignore[misc, assignment]

from langchain_core.tools import BaseTool

from langchain_pubnub import PubNubHistoryTool, PubNubPublishTool, PubNubSubscribeTool

# =============================================================================
# Mock PubNub for Standard Tests
# =============================================================================


def create_mock_pubnub() -> MagicMock:
    """Create a mock PubNub instance for testing."""
    mock = MagicMock()

    # Mock publish
    publish_result = MagicMock()
    publish_result.result.timetoken = 17193163560057793
    mock.publish.return_value.channel.return_value.message.return_value.meta.return_value.sync.return_value = publish_result
    mock.publish.return_value.channel.return_value.message.return_value.sync.return_value = (
        publish_result
    )

    # Mock fetch_messages
    fetch_result = MagicMock()
    fetch_result.result.channels = {"test-channel": []}
    mock.fetch_messages.return_value.channels.return_value.maximum_per_channel.return_value.include_meta.return_value.sync.return_value = fetch_result

    # Mock channel subscription
    subscription_mock = MagicMock()
    mock.channel.return_value.subscription.return_value = subscription_mock

    return mock


# =============================================================================
# Standard Tool Tests using langchain-tests
# =============================================================================


@pytest.mark.skipif(
    not LANGCHAIN_TESTS_AVAILABLE,
    reason="langchain-tests not installed",
)
class TestPubNubPublishToolStandard(ToolsUnitTests):
    """Standard LangChain tests for PubNubPublishTool."""

    @property
    def tool_constructor(self) -> type[BaseTool]:
        """Return the tool class."""
        return PubNubPublishTool

    @property
    def tool_constructor_params(self) -> dict[str, Any]:
        """Return constructor parameters."""
        return {"pubnub": create_mock_pubnub()}

    @property
    def tool_invoke_params_example(self) -> dict[str, Any]:
        """Return example invoke parameters."""
        return {
            "channel": "test-channel",
            "message": {"text": "Hello, World!"},
        }


@pytest.mark.skipif(
    not LANGCHAIN_TESTS_AVAILABLE,
    reason="langchain-tests not installed",
)
class TestPubNubHistoryToolStandard(ToolsUnitTests):
    """Standard LangChain tests for PubNubHistoryTool."""

    @property
    def tool_constructor(self) -> type[BaseTool]:
        """Return the tool class."""
        return PubNubHistoryTool

    @property
    def tool_constructor_params(self) -> dict[str, Any]:
        """Return constructor parameters."""
        return {"pubnub": create_mock_pubnub()}

    @property
    def tool_invoke_params_example(self) -> dict[str, Any]:
        """Return example invoke parameters."""
        return {
            "channels": ["test-channel"],
            "count": 10,
        }


@pytest.mark.skipif(
    not LANGCHAIN_TESTS_AVAILABLE,
    reason="langchain-tests not installed",
)
class TestPubNubSubscribeToolStandard(ToolsUnitTests):
    """Standard LangChain tests for PubNubSubscribeTool."""

    @property
    def tool_constructor(self) -> type[BaseTool]:
        """Return the tool class."""
        return PubNubSubscribeTool

    @property
    def tool_constructor_params(self) -> dict[str, Any]:
        """Return constructor parameters."""
        return {"pubnub": create_mock_pubnub()}

    @property
    def tool_invoke_params_example(self) -> dict[str, Any]:
        """Return example invoke parameters."""
        return {
            "channel": "test-channel",
            "timeout": 1,
            "max_messages": 5,
        }


# =============================================================================
# Fallback tests if langchain-tests is not available
# =============================================================================


class TestToolsConformance:
    """Basic conformance tests that don't require langchain-tests."""

    @pytest.fixture
    def mock_pubnub(self) -> MagicMock:
        """Create a mock PubNub instance."""
        return create_mock_pubnub()

    def test_publish_tool_is_base_tool(self, mock_pubnub: MagicMock) -> None:
        """Verify PubNubPublishTool inherits from BaseTool."""
        tool = PubNubPublishTool(pubnub=mock_pubnub)
        assert isinstance(tool, BaseTool)

    def test_history_tool_is_base_tool(self, mock_pubnub: MagicMock) -> None:
        """Verify PubNubHistoryTool inherits from BaseTool."""
        tool = PubNubHistoryTool(pubnub=mock_pubnub)
        assert isinstance(tool, BaseTool)

    def test_subscribe_tool_is_base_tool(self, mock_pubnub: MagicMock) -> None:
        """Verify PubNubSubscribeTool inherits from BaseTool."""
        tool = PubNubSubscribeTool(pubnub=mock_pubnub)
        assert isinstance(tool, BaseTool)

    def test_all_tools_have_required_attributes(self, mock_pubnub: MagicMock) -> None:
        """Verify all tools have name, description, and args_schema."""
        tools = [
            PubNubPublishTool(pubnub=mock_pubnub),
            PubNubHistoryTool(pubnub=mock_pubnub),
            PubNubSubscribeTool(pubnub=mock_pubnub),
        ]

        for tool in tools:
            assert hasattr(tool, "name"), f"{tool.__class__.__name__} missing name"
            assert hasattr(tool, "description"), f"{tool.__class__.__name__} missing description"
            assert tool.name, f"{tool.__class__.__name__} has empty name"
            assert tool.description, f"{tool.__class__.__name__} has empty description"

    def test_tools_have_unique_names(self, mock_pubnub: MagicMock) -> None:
        """Verify all tools have unique names."""
        tools = [
            PubNubPublishTool(pubnub=mock_pubnub),
            PubNubHistoryTool(pubnub=mock_pubnub),
            PubNubSubscribeTool(pubnub=mock_pubnub),
        ]

        names = [t.name for t in tools]
        assert len(names) == len(set(names)), "Tool names must be unique"

    def test_tools_implement_run(self, mock_pubnub: MagicMock) -> None:
        """Verify all tools implement _run method."""
        tools = [
            PubNubPublishTool(pubnub=mock_pubnub),
            PubNubHistoryTool(pubnub=mock_pubnub),
            PubNubSubscribeTool(pubnub=mock_pubnub),
        ]

        for tool in tools:
            assert hasattr(tool, "_run"), f"{tool.__class__.__name__} missing _run"
            assert callable(tool._run), f"{tool.__class__.__name__}._run not callable"
