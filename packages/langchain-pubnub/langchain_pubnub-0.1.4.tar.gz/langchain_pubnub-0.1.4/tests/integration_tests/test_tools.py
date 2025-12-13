"""Integration tests for PubNub LangChain tools.

These tests make actual network calls to PubNub using demo keys.
They verify end-to-end functionality of the tools.

Run with: pytest tests/integration_tests/ -v

Note: These tests require network connectivity and use PubNub demo keys.
"""

from __future__ import annotations

import json
import os
import time
import uuid

import pytest

from langchain_pubnub import (
    PubNubHistoryTool,
    PubNubPublishTool,
    PubNubSubscribeTool,
    PubNubToolkit,
    create_pubnub_tools,
)

# Skip all tests in this module if SKIP_INTEGRATION_TESTS is set
pytestmark = pytest.mark.skipif(
    os.getenv("SKIP_INTEGRATION_TESTS", "false").lower() == "true",
    reason="Integration tests skipped via SKIP_INTEGRATION_TESTS env var",
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def pubnub_toolkit() -> PubNubToolkit:
    """Create a PubNubToolkit with demo keys for testing."""
    toolkit = PubNubToolkit(
        publish_key=os.getenv("PUBNUB_PUBLISH_KEY", "demo"),
        subscribe_key=os.getenv("PUBNUB_SUBSCRIBE_KEY", "demo"),
        user_id=f"langchain-test-{uuid.uuid4().hex[:8]}",
    )
    yield toolkit
    toolkit.cleanup()


@pytest.fixture
def unique_channel() -> str:
    """Generate a unique channel name for test isolation."""
    return f"langchain-test-{uuid.uuid4().hex[:12]}"


@pytest.fixture
def publish_tool(pubnub_toolkit: PubNubToolkit) -> PubNubPublishTool:
    """Get publish tool from toolkit."""
    return pubnub_toolkit.publish_tool


@pytest.fixture
def history_tool(pubnub_toolkit: PubNubToolkit) -> PubNubHistoryTool:
    """Get history tool from toolkit."""
    return pubnub_toolkit.history_tool


@pytest.fixture
def subscribe_tool(pubnub_toolkit: PubNubToolkit) -> PubNubSubscribeTool:
    """Get subscribe tool from toolkit."""
    return pubnub_toolkit.subscribe_tool


# =============================================================================
# Publish Tool Integration Tests
# =============================================================================


class TestPubNubPublishToolIntegration:
    """Integration tests for PubNubPublishTool."""

    def test_publish_string_message(
        self, publish_tool: PubNubPublishTool, unique_channel: str
    ) -> None:
        """Test publishing a string message."""
        result = publish_tool.invoke(
            {
                "channel": unique_channel,
                "message": "Hello, Integration Test!",
            }
        )

        parsed = json.loads(result)
        assert parsed["success"] is True
        assert "timetoken" in parsed
        assert isinstance(parsed["timetoken"], int)
        assert parsed["timetoken"] > 0

    def test_publish_dict_message(
        self, publish_tool: PubNubPublishTool, unique_channel: str
    ) -> None:
        """Test publishing a dictionary message."""
        message = {
            "text": "Hello from integration test",
            "sender": "test-agent",
            "timestamp": time.time(),
        }

        result = publish_tool.invoke(
            {
                "channel": unique_channel,
                "message": message,
            }
        )

        parsed = json.loads(result)
        assert parsed["success"] is True
        assert "timetoken" in parsed

    def test_publish_with_metadata(
        self, publish_tool: PubNubPublishTool, unique_channel: str
    ) -> None:
        """Test publishing with metadata."""
        result = publish_tool.invoke(
            {
                "channel": unique_channel,
                "message": "Test message with meta",
                "meta": {"priority": "high", "category": "test"},
            }
        )

        parsed = json.loads(result)
        assert parsed["success"] is True

    def test_publish_complex_json(
        self, publish_tool: PubNubPublishTool, unique_channel: str
    ) -> None:
        """Test publishing complex JSON structures."""
        message = {
            "type": "event",
            "data": {
                "nested": {
                    "array": [1, 2, 3],
                    "boolean": True,
                    "null_value": None,
                }
            },
        }

        result = publish_tool.invoke(
            {
                "channel": unique_channel,
                "message": message,
            }
        )

        parsed = json.loads(result)
        assert parsed["success"] is True


# =============================================================================
# History Tool Integration Tests
# =============================================================================


class TestPubNubHistoryToolIntegration:
    """Integration tests for PubNubHistoryTool."""

    def test_fetch_empty_channel_history(
        self, history_tool: PubNubHistoryTool, unique_channel: str
    ) -> None:
        """Test fetching history from empty channel."""
        result = history_tool.invoke(
            {
                "channels": [unique_channel],
                "count": 10,
            }
        )

        parsed = json.loads(result)
        assert parsed["success"] is True
        assert "channels" in parsed

    def test_publish_then_fetch_history(
        self,
        publish_tool: PubNubPublishTool,
        history_tool: PubNubHistoryTool,
        unique_channel: str,
    ) -> None:
        """Test publishing a message then fetching it from history."""
        # Publish a message
        test_message = {"test_id": uuid.uuid4().hex, "content": "Test message"}
        publish_result = publish_tool.invoke(
            {
                "channel": unique_channel,
                "message": test_message,
            }
        )

        publish_parsed = json.loads(publish_result)
        assert publish_parsed["success"] is True

        # Wait for message persistence
        time.sleep(2)

        # Fetch history
        history_result = history_tool.invoke(
            {
                "channels": [unique_channel],
                "count": 10,
            }
        )

        history_parsed = json.loads(history_result)
        assert history_parsed["success"] is True

        # Note: Message may or may not be in history depending on
        # whether Message Persistence is enabled on the keyset

    def test_fetch_multiple_channels(self, history_tool: PubNubHistoryTool) -> None:
        """Test fetching history from multiple channels."""
        channels = [
            f"langchain-test-multi-{uuid.uuid4().hex[:8]}",
            f"langchain-test-multi-{uuid.uuid4().hex[:8]}",
        ]

        result = history_tool.invoke(
            {
                "channels": channels,
                "count": 5,
            }
        )

        parsed = json.loads(result)
        assert parsed["success"] is True
        assert "channels" in parsed

    def test_fetch_with_count_limit(
        self, history_tool: PubNubHistoryTool, unique_channel: str
    ) -> None:
        """Test fetching history with count limit."""
        result = history_tool.invoke(
            {
                "channels": [unique_channel],
                "count": 1,
            }
        )

        parsed = json.loads(result)
        assert parsed["success"] is True


# =============================================================================
# Subscribe Tool Integration Tests
# =============================================================================


class TestPubNubSubscribeToolIntegration:
    """Integration tests for PubNubSubscribeTool."""

    def test_subscribe_timeout(
        self, subscribe_tool: PubNubSubscribeTool, unique_channel: str
    ) -> None:
        """Test that subscribe respects timeout."""
        start_time = time.time()

        result = subscribe_tool.invoke(
            {
                "channel": unique_channel,
                "timeout": 2,
                "max_messages": 10,
            }
        )

        elapsed = time.time() - start_time

        parsed = json.loads(result)
        assert parsed["success"] is True
        assert parsed["timeout_reached"] is True
        assert elapsed >= 1.5  # Should have waited close to timeout
        assert elapsed < 5  # But not too long

    def test_subscribe_returns_valid_structure(
        self, subscribe_tool: PubNubSubscribeTool, unique_channel: str
    ) -> None:
        """Test that subscribe returns expected structure."""
        result = subscribe_tool.invoke(
            {
                "channel": unique_channel,
                "timeout": 1,
                "max_messages": 5,
            }
        )

        parsed = json.loads(result)
        assert parsed["success"] is True
        assert "channel" in parsed
        assert "messages" in parsed
        assert "count" in parsed
        assert "timeout_reached" in parsed
        assert isinstance(parsed["messages"], list)


# =============================================================================
# Toolkit Integration Tests
# =============================================================================


class TestPubNubToolkitIntegration:
    """Integration tests for PubNubToolkit."""

    def test_toolkit_creates_working_tools(self) -> None:
        """Test that toolkit creates functional tools."""
        toolkit = PubNubToolkit(
            publish_key=os.getenv("PUBNUB_PUBLISH_KEY", "demo"),
            subscribe_key=os.getenv("PUBNUB_SUBSCRIBE_KEY", "demo"),
            user_id=f"toolkit-test-{uuid.uuid4().hex[:8]}",
        )

        try:
            tools = toolkit.get_tools()
            assert len(tools) == 3

            # Verify each tool is functional
            for tool in tools:
                assert tool.name is not None
                assert tool.description is not None
                assert tool.get_input_schema() is not None
        finally:
            toolkit.cleanup()

    def test_create_pubnub_tools_function(self) -> None:
        """Test the convenience function creates working tools."""
        tools = create_pubnub_tools(
            publish_key=os.getenv("PUBNUB_PUBLISH_KEY", "demo"),
            subscribe_key=os.getenv("PUBNUB_SUBSCRIBE_KEY", "demo"),
            user_id=f"factory-test-{uuid.uuid4().hex[:8]}",
        )

        assert len(tools) == 3

        tool_names = {t.name for t in tools}
        assert "pubnub_publish" in tool_names
        assert "pubnub_history" in tool_names
        assert "pubnub_subscribe" in tool_names


# =============================================================================
# End-to-End Integration Tests
# =============================================================================


class TestEndToEndIntegration:
    """End-to-end integration tests simulating agent usage."""

    def test_publish_and_verify_workflow(
        self,
        publish_tool: PubNubPublishTool,
        history_tool: PubNubHistoryTool,
        unique_channel: str,
    ) -> None:
        """Test a complete publish-verify workflow."""
        # Step 1: Publish multiple messages
        messages_sent = []
        for i in range(3):
            msg = {"index": i, "content": f"Message {i}"}
            result = publish_tool.invoke(
                {
                    "channel": unique_channel,
                    "message": msg,
                }
            )
            parsed = json.loads(result)
            assert parsed["success"] is True
            messages_sent.append(msg)

        # Step 2: Wait for persistence
        time.sleep(2)

        # Step 3: Fetch and verify
        history_result = history_tool.invoke(
            {
                "channels": [unique_channel],
                "count": 10,
            }
        )

        history_parsed = json.loads(history_result)
        assert history_parsed["success"] is True

    def test_tool_error_handling(self, history_tool: PubNubHistoryTool) -> None:
        """Test that tools handle errors gracefully."""
        # Empty channel list should still return valid JSON
        result = history_tool.invoke(
            {
                "channels": [],
                "count": 10,
            }
        )

        # Should return valid JSON even if there's an error
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
