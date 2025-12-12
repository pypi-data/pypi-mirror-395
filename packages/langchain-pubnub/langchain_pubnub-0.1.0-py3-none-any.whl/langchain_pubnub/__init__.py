"""LangChain PubNub Integration.

This package provides LangChain tools for interacting with PubNub's
real-time messaging platform.

Tools:
    - PubNubPublishTool: Publish messages to PubNub channels
    - PubNubHistoryTool: Fetch message history from channels
    - PubNubSubscribeTool: Subscribe and collect real-time messages

Example:
    >>> from langchain_pubnub import create_pubnub_tools
    >>> tools = create_pubnub_tools(
    ...     publish_key="demo",
    ...     subscribe_key="demo",
    ...     user_id="my-agent"
    ... )
"""

from langchain_pubnub.tools import (
    PubNubHistoryTool,
    PubNubPublishTool,
    PubNubSubscribeTool,
    PubNubToolkit,
    create_pubnub_tools,
)

__all__ = [
    "PubNubPublishTool",
    "PubNubHistoryTool",
    "PubNubSubscribeTool",
    "PubNubToolkit",
    "create_pubnub_tools",
]

__version__ = "0.1.0"
