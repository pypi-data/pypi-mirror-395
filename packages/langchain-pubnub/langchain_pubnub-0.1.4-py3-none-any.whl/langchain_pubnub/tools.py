"""LangChain PubNub Tool.

A LangChain tool for interacting with PubNub's real-time messaging platform.
Provides publish, subscribe, and history operations for LangChain agents.

Requirements:
    pip install pubnub langchain-core pydantic
"""

from __future__ import annotations

import json
import threading
import time
from typing import TYPE_CHECKING, Any, Optional, Union

from langchain_core.tools import BaseTool
from pubnub.exceptions import PubNubException
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from langchain_core.callbacks import CallbackManagerForToolRun


class PubNubPublishInput(BaseModel):
    """Input schema for PubNub publish operation."""

    channel: str = Field(description="The channel name to publish the message to")
    message: Union[str, dict[str, Any]] = Field(
        description="The message to publish. Can be a string or a JSON-serializable dictionary"
    )
    meta: Optional[dict[str, Any]] = Field(
        default=None,
        description="Optional metadata to include with the message for filtering",
    )


class PubNubHistoryInput(BaseModel):
    """Input schema for PubNub history operation."""

    channels: list[str] = Field(description="List of channel names to fetch history from")
    count: int = Field(
        default=25,
        description="Number of messages to retrieve per channel (max 100 for single channel, 25 for multiple)",
    )
    include_meta: bool = Field(
        default=False,
        description="Whether to include message metadata in the response",
    )
    start: Optional[int] = Field(
        default=None,
        description="Timetoken to start fetching from (exclusive, for pagination)",
    )
    end: Optional[int] = Field(
        default=None,
        description="Timetoken to fetch up to (inclusive)",
    )


class PubNubSubscribeInput(BaseModel):
    """Input schema for PubNub subscribe operation."""

    channel: str = Field(description="The channel name to subscribe to")
    timeout: int = Field(
        default=300,
        description="Maximum time in seconds to wait for messages",
    )
    max_messages: int = Field(
        default=10,
        description="Maximum number of messages to collect before returning",
    )


class PubNubPublishTool(BaseTool):
    """Tool for publishing messages to a PubNub channel.

    Use this tool when you need to send real-time messages to subscribers
    on a specific channel.
    """

    name: str = "pubnub_publish"
    description: str = (
        "Publish a message to a PubNub channel. Use this to send real-time messages "
        "to all subscribers of a channel. Messages must be JSON-serializable and "
        "under 32KB. Returns the publish timetoken on success."
    )
    args_schema: type[BaseModel] = PubNubPublishInput

    pubnub: Any = Field(exclude=True)

    def __init__(self, pubnub: PubNub, **kwargs: Any) -> None:
        """Initialize the publish tool with a PubNub instance."""
        super().__init__(pubnub=pubnub, **kwargs)

    def _run(
        self,
        channel: str,
        message: Union[str, dict[str, Any]],
        meta: Optional[dict[str, Any]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the publish operation."""
        try:
            publish_builder = self.pubnub.publish().channel(channel).message(message)

            if meta:
                publish_builder = publish_builder.meta(meta)

            envelope = publish_builder.sync()

            return json.dumps(
                {
                    "success": True,
                    "timetoken": envelope.result.timetoken,
                    "channel": channel,
                    "message": "Message published successfully",
                }
            )
        except PubNubException as e:
            return json.dumps(
                {
                    "success": False,
                    "error": str(e),
                    "channel": channel,
                }
            )


class PubNubHistoryTool(BaseTool):
    """Tool for fetching message history from PubNub channels.

    Use this tool when you need to retrieve past messages from one or more channels.
    Requires Message Persistence to be enabled on your PubNub keyset.
    """

    name: str = "pubnub_history"
    description: str = (
        "Fetch historical messages from PubNub channels. Use this to retrieve "
        "past messages from one or more channels. Returns messages with their "
        "content, timetoken, and optional metadata. Max 100 messages per channel "
        "for single channel, 25 for multiple channels."
    )
    args_schema: type[BaseModel] = PubNubHistoryInput

    pubnub: Any = Field(exclude=True)

    def __init__(self, pubnub: PubNub, **kwargs: Any) -> None:
        """Initialize the history tool with a PubNub instance."""
        super().__init__(pubnub=pubnub, **kwargs)

    def _run(
        self,
        channels: list[str],
        count: int = 25,
        include_meta: bool = False,
        start: Optional[int] = None,
        end: Optional[int] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the history fetch operation."""
        try:
            fetch_builder = (
                self.pubnub.fetch_messages()
                .channels(channels)
                .maximum_per_channel(count)
                .include_meta(include_meta)
            )

            if start is not None:
                fetch_builder = fetch_builder.start(start)
            if end is not None:
                fetch_builder = fetch_builder.end(end)

            envelope = fetch_builder.sync()

            # Format the results
            result: dict[str, Any] = {
                "success": True,
                "channels": {},
            }

            for channel_name, messages in envelope.result.channels.items():
                result["channels"][channel_name] = [
                    {
                        "message": msg.message,
                        "timetoken": msg.timetoken,
                        "meta": msg.meta if include_meta else None,
                    }
                    for msg in messages
                ]

            return json.dumps(result)
        except PubNubException as e:
            return json.dumps(
                {
                    "success": False,
                    "error": str(e),
                    "channels": channels,
                }
            )


class MessageCollector(SubscribeListener):
    """Listener that collects messages for the subscribe tool."""

    def __init__(self, max_messages: int = 10) -> None:
        """Initialize the message collector."""
        super().__init__()
        self.messages: list[dict[str, Any]] = []
        self.max_messages = max_messages
        self.lock = threading.Lock()

    def status(self, pubnub: Any, status: Any) -> None:
        """Handle status changes silently."""

    def message(self, pubnub: Any, message: Any) -> None:
        """Collect incoming messages."""
        with self.lock:
            if len(self.messages) < self.max_messages:
                self.messages.append(
                    {
                        "channel": message.channel,
                        "message": message.message,
                        "timetoken": message.timetoken,
                        "publisher": message.publisher,
                    }
                )

    def presence(self, pubnub: Any, presence: Any) -> None:
        """Handle presence events (not collected)."""


class PubNubSubscribeTool(BaseTool):
    """Tool for subscribing to a PubNub channel and collecting messages.

    Use this tool when you need to listen for real-time messages on a channel.
    This is a blocking operation that waits for messages up to a timeout.
    """

    name: str = "pubnub_subscribe"
    description: str = (
        "Subscribe to a PubNub channel and collect real-time messages. "
        "This will listen for messages for the specified timeout period "
        "or until max_messages are received. Returns collected messages. "
        "Use this when you need to receive live messages from a channel."
    )
    args_schema: type[BaseModel] = PubNubSubscribeInput

    pubnub: Any = Field(exclude=True)

    def __init__(self, pubnub: PubNub, **kwargs: Any) -> None:
        """Initialize the subscribe tool with a PubNub instance."""
        super().__init__(pubnub=pubnub, **kwargs)

    def _run(
        self,
        channel: str,
        timeout: int = 300,
        max_messages: int = 10,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the subscribe operation."""
        try:
            collector = MessageCollector(max_messages=max_messages)

            # Create subscription
            subscription = self.pubnub.channel(channel).subscription()

            # Set up message handler
            subscription.on_message = lambda msg: collector.message(self.pubnub, msg)

            # Subscribe
            subscription.subscribe()

            # Wait for messages or timeout
            start_time = time.time()
            while time.time() - start_time < timeout:
                if len(collector.messages) >= max_messages:
                    break
                time.sleep(0.1)

            # Unsubscribe
            subscription.unsubscribe()

            return json.dumps(
                {
                    "success": True,
                    "channel": channel,
                    "messages": collector.messages,
                    "count": len(collector.messages),
                    "timeout_reached": len(collector.messages) < max_messages,
                }
            )
        except PubNubException as e:
            return json.dumps(
                {
                    "success": False,
                    "error": str(e),
                    "channel": channel,
                }
            )


class PubNubToolkit:
    """A toolkit that provides all PubNub tools for LangChain agents.

    Usage:
        from langchain_pubnub import PubNubToolkit

        toolkit = PubNubToolkit(
            publish_key="your-publish-key",
            subscribe_key="your-subscribe-key",
            user_id="your-user-id"
        )

        tools = toolkit.get_tools()
        # Use tools with your LangChain agent
    """

    def __init__(
        self,
        publish_key: str,
        subscribe_key: str,
        user_id: str,
        ssl: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize the PubNub toolkit.

        Args:
            publish_key: Your PubNub publish key
            subscribe_key: Your PubNub subscribe key
            user_id: Unique identifier for this client
            ssl: Whether to use SSL (default True)
            **kwargs: Additional PNConfiguration options
        """
        pnconfig = PNConfiguration()
        pnconfig.publish_key = publish_key
        pnconfig.subscribe_key = subscribe_key
        pnconfig.user_id = user_id
        pnconfig.ssl = ssl

        # Apply any additional configuration
        for key, value in kwargs.items():
            if hasattr(pnconfig, key):
                setattr(pnconfig, key, value)

        self.pubnub = PubNub(pnconfig)

        # Initialize tools
        self._publish_tool = PubNubPublishTool(pubnub=self.pubnub)
        self._history_tool = PubNubHistoryTool(pubnub=self.pubnub)
        self._subscribe_tool = PubNubSubscribeTool(pubnub=self.pubnub)

    def get_tools(self) -> list[BaseTool]:
        """Get all PubNub tools as a list."""
        return [
            self._publish_tool,
            self._history_tool,
            self._subscribe_tool,
        ]

    @property
    def publish_tool(self) -> PubNubPublishTool:
        """Get the publish tool."""
        return self._publish_tool

    @property
    def history_tool(self) -> PubNubHistoryTool:
        """Get the history tool."""
        return self._history_tool

    @property
    def subscribe_tool(self) -> PubNubSubscribeTool:
        """Get the subscribe tool."""
        return self._subscribe_tool

    def cleanup(self) -> None:
        """Clean up PubNub resources."""
        self.pubnub.stop()


def create_pubnub_tools(
    publish_key: str,
    subscribe_key: str,
    user_id: str,
    **kwargs: Any,
) -> list[BaseTool]:
    """Create PubNub tools for use with LangChain agents.

    Args:
        publish_key: Your PubNub publish key
        subscribe_key: Your PubNub subscribe key
        user_id: Unique identifier for this client
        **kwargs: Additional PNConfiguration options

    Returns:
        List of PubNub tools (publish, history, subscribe)

    Example:
        from langchain_pubnub import create_pubnub_tools

        tools = create_pubnub_tools(
            publish_key="pub-c-xxx",
            subscribe_key="sub-c-xxx",
            user_id="my-agent"
        )

        # Add to your agent
        agent = create_react_agent(llm, tools, prompt)
    """
    toolkit = PubNubToolkit(
        publish_key=publish_key,
        subscribe_key=subscribe_key,
        user_id=user_id,
        **kwargs,
    )
    return toolkit.get_tools()
