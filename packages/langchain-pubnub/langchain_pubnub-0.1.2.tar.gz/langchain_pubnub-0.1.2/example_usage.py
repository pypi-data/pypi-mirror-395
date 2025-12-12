"""Example usage of the LangChain PubNub Tool.

This example demonstrates how to use the PubNub tools with a LangChain agent.

Requirements:
    pip install pubnub langchain-core langchain-openai pydantic

Set your environment variables:
    export OPENAI_API_KEY="your-openai-key"
    export PUBNUB_PUBLISH_KEY="your-publish-key"  # or use 'demo'
    export PUBNUB_SUBSCRIBE_KEY="your-subscribe-key"  # or use 'demo'
"""

import os

from langchain_pubnub import PubNubToolkit, create_pubnub_tools

# ============================================================================
# Example 1: Basic Tool Usage (without LLM)
# ============================================================================


def basic_usage_example() -> None:
    """Demonstrate basic PubNub tool usage without an LLM agent."""
    print("=" * 60)
    print("Example 1: Basic Tool Usage")
    print("=" * 60)

    # Create toolkit with demo keys (or use your own)
    toolkit = PubNubToolkit(
        publish_key=os.getenv("PUBNUB_PUBLISH_KEY", "demo"),
        subscribe_key=os.getenv("PUBNUB_SUBSCRIBE_KEY", "demo"),
        user_id="langchain-example-user",
    )

    # Get individual tools
    publish_tool = toolkit.publish_tool
    history_tool = toolkit.history_tool

    # Publish a message
    print("\n1. Publishing a message...")
    result = publish_tool.invoke(
        {
            "channel": "langchain-test",
            "message": {"text": "Hello from LangChain!", "sender": "example-agent"},
        }
    )
    print(f"Publish result: {result}")

    # Fetch history
    print("\n2. Fetching message history...")
    result = history_tool.invoke(
        {
            "channels": ["langchain-test"],
            "count": 5,
            "include_meta": False,
        }
    )
    print(f"History result: {result}")

    # Cleanup
    toolkit.cleanup()
    print("\nBasic usage example completed!")


# ============================================================================
# Example 2: Using with LangChain Agent
# ============================================================================


def agent_usage_example() -> None:
    """Demonstrate PubNub tools with a LangChain agent."""
    print("\n" + "=" * 60)
    print("Example 2: LangChain Agent Usage")
    print("=" * 60)

    try:
        from langchain.agents import AgentExecutor, create_react_agent
        from langchain_core.prompts import PromptTemplate
        from langchain_openai import ChatOpenAI
    except ImportError:
        print("This example requires langchain-openai. Install with:")
        print("  pip install langchain-openai")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("Set OPENAI_API_KEY environment variable to run this example")
        return

    # Create PubNub tools
    tools = create_pubnub_tools(
        publish_key=os.getenv("PUBNUB_PUBLISH_KEY", "demo"),
        subscribe_key=os.getenv("PUBNUB_SUBSCRIBE_KEY", "demo"),
        user_id="langchain-agent",
    )

    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Create a prompt template
    prompt = PromptTemplate.from_template(
        """You are a helpful assistant with access to PubNub real-time messaging tools.

You have access to the following tools:
{tools}

Tool names: {tool_names}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
    )

    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Example queries
    print("\n--- Agent Query 1: Publish a message ---")
    agent_executor.invoke(
        {"input": "Send a greeting message to the 'announcements' channel saying 'Hello everyone!'"}
    )

    print("\n--- Agent Query 2: Get message history ---")
    agent_executor.invoke({"input": "What are the last 3 messages on the 'announcements' channel?"})


# ============================================================================
# Example 3: Function-based Tool (simpler alternative)
# ============================================================================


def function_tool_example() -> None:
    """Demonstrate creating function-based tools."""
    print("\n" + "=" * 60)
    print("Example 3: Function-based Tool")
    print("=" * 60)

    from langchain_core.tools import tool
    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub

    # Initialize PubNub
    pnconfig = PNConfiguration()
    pnconfig.publish_key = os.getenv("PUBNUB_PUBLISH_KEY", "demo")
    pnconfig.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY", "demo")
    pnconfig.user_id = "function-tool-user"
    pubnub = PubNub(pnconfig)

    @tool
    def publish_message(channel: str, message: str) -> str:
        """Publish a message to a PubNub channel.

        Args:
            channel: The channel name to publish to
            message: The message text to send

        Returns:
            Result of the publish operation
        """
        try:
            envelope = pubnub.publish().channel(channel).message({"text": message}).sync()
            return f"Message published successfully. Timetoken: {envelope.result.timetoken}"
        except Exception as e:
            return f"Failed to publish: {e!s}"

    @tool
    def get_channel_history(channel: str, count: int = 10) -> str:
        """Get message history from a PubNub channel.

        Args:
            channel: The channel name to fetch history from
            count: Number of messages to retrieve (default 10)

        Returns:
            List of recent messages from the channel
        """
        try:
            envelope = pubnub.fetch_messages().channels([channel]).maximum_per_channel(count).sync()
            messages = envelope.result.channels.get(channel, [])
            return str([{"message": m.message, "time": m.timetoken} for m in messages])
        except Exception as e:
            return f"Failed to fetch history: {e!s}"

    # Test the function tools
    print("\nPublishing a test message...")
    result = publish_message.invoke(
        {
            "channel": "test-channel",
            "message": "Test from function tool!",
        }
    )
    print(f"Result: {result}")

    print("\nFetching history...")
    result = get_channel_history.invoke({"channel": "test-channel", "count": 3})
    print(f"Result: {result}")

    pubnub.stop()
    print("\nFunction-based tool example completed!")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("LangChain PubNub Tool Examples")
    print("=" * 60)

    # Run basic example (always works)
    basic_usage_example()

    # Run function-based example
    function_tool_example()

    # Run agent example (requires OpenAI key)
    # Uncomment the line below to run with an agent
    # agent_usage_example()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
