"""Unit tests for PubNub LangChain tools.

These tests follow LangChain's standard testing patterns for tools.
They test tool initialization, schema validation, and basic functionality
without making actual network calls.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.tools import BaseTool
from pydantic import BaseModel, ValidationError

from langchain_pubnub import (
    PubNubHistoryTool,
    PubNubPublishTool,
    PubNubSubscribeTool,
    PubNubToolkit,
    create_pubnub_tools,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_pubnub() -> MagicMock:
    """Create a mock PubNub instance."""
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
    fetch_result.result.channels = {
        "test-channel": [MagicMock(message={"text": "Hello"}, timetoken=123456789, meta=None)]
    }
    mock.fetch_messages.return_value.channels.return_value.maximum_per_channel.return_value.include_meta.return_value.sync.return_value = fetch_result
    mock.fetch_messages.return_value.channels.return_value.maximum_per_channel.return_value.include_meta.return_value.start.return_value.sync.return_value = fetch_result
    mock.fetch_messages.return_value.channels.return_value.maximum_per_channel.return_value.include_meta.return_value.end.return_value.sync.return_value = fetch_result

    # Mock channel subscription
    subscription_mock = MagicMock()
    mock.channel.return_value.subscription.return_value = subscription_mock

    return mock


@pytest.fixture
def publish_tool(mock_pubnub: MagicMock) -> PubNubPublishTool:
    """Create a PubNubPublishTool with mocked PubNub."""
    return PubNubPublishTool(pubnub=mock_pubnub)


@pytest.fixture
def history_tool(mock_pubnub: MagicMock) -> PubNubHistoryTool:
    """Create a PubNubHistoryTool with mocked PubNub."""
    return PubNubHistoryTool(pubnub=mock_pubnub)


@pytest.fixture
def subscribe_tool(mock_pubnub: MagicMock) -> PubNubSubscribeTool:
    """Create a PubNubSubscribeTool with mocked PubNub."""
    return PubNubSubscribeTool(pubnub=mock_pubnub)


# =============================================================================
# PubNubPublishTool Tests
# =============================================================================


class TestPubNubPublishTool:
    """Tests for PubNubPublishTool following LangChain standards."""

    def test_init(self, publish_tool: PubNubPublishTool) -> None:
        """Test that the tool can be instantiated."""
        assert publish_tool is not None
        assert isinstance(publish_tool, BaseTool)

    def test_has_name(self, publish_tool: PubNubPublishTool) -> None:
        """Test that the tool has a name attribute."""
        assert hasattr(publish_tool, "name")
        assert publish_tool.name == "pubnub_publish"
        assert isinstance(publish_tool.name, str)
        assert len(publish_tool.name) > 0

    def test_has_description(self, publish_tool: PubNubPublishTool) -> None:
        """Test that the tool has a description."""
        assert hasattr(publish_tool, "description")
        assert isinstance(publish_tool.description, str)
        assert len(publish_tool.description) > 0

    def test_has_input_schema(self, publish_tool: PubNubPublishTool) -> None:
        """Test that the tool has a valid input schema."""
        schema = publish_tool.get_input_schema()
        assert schema is not None
        assert issubclass(schema, BaseModel)

    def test_input_schema_has_required_fields(self, publish_tool: PubNubPublishTool) -> None:
        """Test that input schema has required fields."""
        schema = publish_tool.get_input_schema()
        schema_fields = schema.model_fields

        assert "channel" in schema_fields
        assert "message" in schema_fields

    def test_input_schema_matches_invoke_params(self, publish_tool: PubNubPublishTool) -> None:
        """Test that example params match the input schema."""
        example_params = {
            "channel": "test-channel",
            "message": {"text": "Hello, World!"},
        }
        schema = publish_tool.get_input_schema()
        # This should not raise
        schema(**example_params)

    def test_invoke_returns_json(
        self, publish_tool: PubNubPublishTool, mock_pubnub: MagicMock
    ) -> None:
        """Test that invoke returns valid JSON."""
        result = publish_tool.invoke(
            {
                "channel": "test-channel",
                "message": "Hello",
            }
        )

        # Should be valid JSON
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
        assert "success" in parsed

    def test_invoke_success_response(
        self, publish_tool: PubNubPublishTool, mock_pubnub: MagicMock
    ) -> None:
        """Test successful publish response structure."""
        result = publish_tool.invoke(
            {
                "channel": "test-channel",
                "message": {"text": "Hello"},
            }
        )

        parsed = json.loads(result)
        assert parsed["success"] is True
        assert "timetoken" in parsed
        assert parsed["channel"] == "test-channel"

    def test_invoke_with_meta(
        self, publish_tool: PubNubPublishTool, mock_pubnub: MagicMock
    ) -> None:
        """Test publish with metadata."""
        result = publish_tool.invoke(
            {
                "channel": "test-channel",
                "message": "Hello",
                "meta": {"sender": "test-user"},
            }
        )

        parsed = json.loads(result)
        assert parsed["success"] is True


# =============================================================================
# PubNubHistoryTool Tests
# =============================================================================


class TestPubNubHistoryTool:
    """Tests for PubNubHistoryTool following LangChain standards."""

    def test_init(self, history_tool: PubNubHistoryTool) -> None:
        """Test that the tool can be instantiated."""
        assert history_tool is not None
        assert isinstance(history_tool, BaseTool)

    def test_has_name(self, history_tool: PubNubHistoryTool) -> None:
        """Test that the tool has a name attribute."""
        assert hasattr(history_tool, "name")
        assert history_tool.name == "pubnub_history"
        assert isinstance(history_tool.name, str)
        assert len(history_tool.name) > 0

    def test_has_description(self, history_tool: PubNubHistoryTool) -> None:
        """Test that the tool has a description."""
        assert hasattr(history_tool, "description")
        assert isinstance(history_tool.description, str)
        assert len(history_tool.description) > 0

    def test_has_input_schema(self, history_tool: PubNubHistoryTool) -> None:
        """Test that the tool has a valid input schema."""
        schema = history_tool.get_input_schema()
        assert schema is not None
        assert issubclass(schema, BaseModel)

    def test_input_schema_has_required_fields(self, history_tool: PubNubHistoryTool) -> None:
        """Test that input schema has required fields."""
        schema = history_tool.get_input_schema()
        schema_fields = schema.model_fields

        assert "channels" in schema_fields

    def test_input_schema_matches_invoke_params(self, history_tool: PubNubHistoryTool) -> None:
        """Test that example params match the input schema."""
        example_params = {
            "channels": ["test-channel"],
            "count": 10,
        }
        schema = history_tool.get_input_schema()
        # This should not raise
        schema(**example_params)

    def test_invoke_returns_json(
        self, history_tool: PubNubHistoryTool, mock_pubnub: MagicMock
    ) -> None:
        """Test that invoke returns valid JSON."""
        result = history_tool.invoke(
            {
                "channels": ["test-channel"],
            }
        )

        parsed = json.loads(result)
        assert isinstance(parsed, dict)
        assert "success" in parsed

    def test_invoke_success_response(
        self, history_tool: PubNubHistoryTool, mock_pubnub: MagicMock
    ) -> None:
        """Test successful history fetch response structure."""
        result = history_tool.invoke(
            {
                "channels": ["test-channel"],
                "count": 5,
            }
        )

        parsed = json.loads(result)
        assert parsed["success"] is True
        assert "channels" in parsed


# =============================================================================
# PubNubSubscribeTool Tests
# =============================================================================


class TestPubNubSubscribeTool:
    """Tests for PubNubSubscribeTool following LangChain standards."""

    def test_init(self, subscribe_tool: PubNubSubscribeTool) -> None:
        """Test that the tool can be instantiated."""
        assert subscribe_tool is not None
        assert isinstance(subscribe_tool, BaseTool)

    def test_has_name(self, subscribe_tool: PubNubSubscribeTool) -> None:
        """Test that the tool has a name attribute."""
        assert hasattr(subscribe_tool, "name")
        assert subscribe_tool.name == "pubnub_subscribe"
        assert isinstance(subscribe_tool.name, str)
        assert len(subscribe_tool.name) > 0

    def test_has_description(self, subscribe_tool: PubNubSubscribeTool) -> None:
        """Test that the tool has a description."""
        assert hasattr(subscribe_tool, "description")
        assert isinstance(subscribe_tool.description, str)
        assert len(subscribe_tool.description) > 0

    def test_has_input_schema(self, subscribe_tool: PubNubSubscribeTool) -> None:
        """Test that the tool has a valid input schema."""
        schema = subscribe_tool.get_input_schema()
        assert schema is not None
        assert issubclass(schema, BaseModel)

    def test_input_schema_has_required_fields(self, subscribe_tool: PubNubSubscribeTool) -> None:
        """Test that input schema has required fields."""
        schema = subscribe_tool.get_input_schema()
        schema_fields = schema.model_fields

        assert "channel" in schema_fields

    def test_input_schema_matches_invoke_params(self, subscribe_tool: PubNubSubscribeTool) -> None:
        """Test that example params match the input schema."""
        example_params = {
            "channel": "test-channel",
            "timeout": 1,
            "max_messages": 5,
        }
        schema = subscribe_tool.get_input_schema()
        # This should not raise
        schema(**example_params)


# =============================================================================
# PubNubToolkit Tests
# =============================================================================


class TestPubNubToolkit:
    """Tests for PubNubToolkit."""

    @patch("langchain_pubnub.tools.PubNub")
    @patch("langchain_pubnub.tools.PNConfiguration")
    def test_init(self, mock_config_class: MagicMock, mock_pubnub_class: MagicMock) -> None:
        """Test toolkit initialization."""
        toolkit = PubNubToolkit(
            publish_key="test-pub-key",
            subscribe_key="test-sub-key",
            user_id="test-user",
        )

        assert toolkit is not None
        mock_config_class.assert_called_once()

    @patch("langchain_pubnub.tools.PubNub")
    @patch("langchain_pubnub.tools.PNConfiguration")
    def test_get_tools_returns_list(
        self, mock_config_class: MagicMock, mock_pubnub_class: MagicMock
    ) -> None:
        """Test that get_tools returns a list of tools."""
        toolkit = PubNubToolkit(
            publish_key="test-pub-key",
            subscribe_key="test-sub-key",
            user_id="test-user",
        )

        tools = toolkit.get_tools()

        assert isinstance(tools, list)
        assert len(tools) == 3
        assert all(isinstance(t, BaseTool) for t in tools)

    @patch("langchain_pubnub.tools.PubNub")
    @patch("langchain_pubnub.tools.PNConfiguration")
    def test_get_tools_contains_all_tools(
        self, mock_config_class: MagicMock, mock_pubnub_class: MagicMock
    ) -> None:
        """Test that get_tools contains all expected tools."""
        toolkit = PubNubToolkit(
            publish_key="test-pub-key",
            subscribe_key="test-sub-key",
            user_id="test-user",
        )

        tools = toolkit.get_tools()
        tool_names = [t.name for t in tools]

        assert "pubnub_publish" in tool_names
        assert "pubnub_history" in tool_names
        assert "pubnub_subscribe" in tool_names

    @patch("langchain_pubnub.tools.PubNub")
    @patch("langchain_pubnub.tools.PNConfiguration")
    def test_individual_tool_properties(
        self, mock_config_class: MagicMock, mock_pubnub_class: MagicMock
    ) -> None:
        """Test individual tool property accessors."""
        toolkit = PubNubToolkit(
            publish_key="test-pub-key",
            subscribe_key="test-sub-key",
            user_id="test-user",
        )

        assert isinstance(toolkit.publish_tool, PubNubPublishTool)
        assert isinstance(toolkit.history_tool, PubNubHistoryTool)
        assert isinstance(toolkit.subscribe_tool, PubNubSubscribeTool)

    @patch("langchain_pubnub.tools.PubNub")
    @patch("langchain_pubnub.tools.PNConfiguration")
    def test_cleanup(self, mock_config_class: MagicMock, mock_pubnub_class: MagicMock) -> None:
        """Test cleanup method."""
        toolkit = PubNubToolkit(
            publish_key="test-pub-key",
            subscribe_key="test-sub-key",
            user_id="test-user",
        )

        toolkit.cleanup()

        toolkit.pubnub.stop.assert_called_once()


# =============================================================================
# create_pubnub_tools Tests
# =============================================================================


class TestCreatePubNubTools:
    """Tests for create_pubnub_tools factory function."""

    @patch("langchain_pubnub.tools.PubNub")
    @patch("langchain_pubnub.tools.PNConfiguration")
    def test_returns_list_of_tools(
        self, mock_config_class: MagicMock, mock_pubnub_class: MagicMock
    ) -> None:
        """Test that function returns a list of tools."""
        tools = create_pubnub_tools(
            publish_key="test-pub-key",
            subscribe_key="test-sub-key",
            user_id="test-user",
        )

        assert isinstance(tools, list)
        assert len(tools) == 3
        assert all(isinstance(t, BaseTool) for t in tools)

    @patch("langchain_pubnub.tools.PubNub")
    @patch("langchain_pubnub.tools.PNConfiguration")
    def test_tools_have_unique_names(
        self, mock_config_class: MagicMock, mock_pubnub_class: MagicMock
    ) -> None:
        """Test that all tools have unique names."""
        tools = create_pubnub_tools(
            publish_key="test-pub-key",
            subscribe_key="test-sub-key",
            user_id="test-user",
        )

        tool_names = [t.name for t in tools]
        assert len(tool_names) == len(set(tool_names))


# =============================================================================
# Schema Validation Tests
# =============================================================================


class TestSchemaValidation:
    """Tests for input schema validation."""

    def test_publish_schema_rejects_missing_channel(self) -> None:
        """Test that publish schema requires channel."""
        from langchain_pubnub.tools import PubNubPublishInput

        with pytest.raises(ValidationError):
            PubNubPublishInput(message="test")  # type: ignore[call-arg]

    def test_publish_schema_rejects_missing_message(self) -> None:
        """Test that publish schema requires message."""
        from langchain_pubnub.tools import PubNubPublishInput

        with pytest.raises(ValidationError):
            PubNubPublishInput(channel="test")  # type: ignore[call-arg]

    def test_history_schema_rejects_missing_channels(self) -> None:
        """Test that history schema requires channels."""
        from langchain_pubnub.tools import PubNubHistoryInput

        with pytest.raises(ValidationError):
            PubNubHistoryInput()  # type: ignore[call-arg]

    def test_subscribe_schema_rejects_missing_channel(self) -> None:
        """Test that subscribe schema requires channel."""
        from langchain_pubnub.tools import PubNubSubscribeInput

        with pytest.raises(ValidationError):
            PubNubSubscribeInput()  # type: ignore[call-arg]

    def test_publish_schema_accepts_dict_message(self) -> None:
        """Test that publish schema accepts dict messages."""
        from langchain_pubnub.tools import PubNubPublishInput

        schema = PubNubPublishInput(
            channel="test",
            message={"key": "value"},
        )
        assert schema.message == {"key": "value"}

    def test_publish_schema_accepts_string_message(self) -> None:
        """Test that publish schema accepts string messages."""
        from langchain_pubnub.tools import PubNubPublishInput

        schema = PubNubPublishInput(
            channel="test",
            message="hello",
        )
        assert schema.message == "hello"

    def test_history_schema_default_values(self) -> None:
        """Test history schema default values."""
        from langchain_pubnub.tools import PubNubHistoryInput

        schema = PubNubHistoryInput(channels=["test"])
        assert schema.count == 25
        assert schema.include_meta is False
        assert schema.start is None
        assert schema.end is None

    def test_subscribe_schema_default_values(self) -> None:
        """Test subscribe schema default values."""
        from langchain_pubnub.tools import PubNubSubscribeInput

        schema = PubNubSubscribeInput(channel="test")
        assert schema.timeout == 300
        assert schema.max_messages == 10
