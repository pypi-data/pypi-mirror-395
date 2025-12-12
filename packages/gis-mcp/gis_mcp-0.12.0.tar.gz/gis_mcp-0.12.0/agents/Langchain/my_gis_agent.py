"""
GIS Agent Implementation

A LangChain-based agent that connects to the GIS MCP (Model Context Protocol) server
via MultiServerMCPClient to provide geospatial analysis capabilities.

This agent utilizes OpenRouter API for language model access and integrates with
the GIS MCP server to perform various geospatial operations including coordinate
transformations, distance calculations, spatial analysis, and geometric operations.

Documentation:
    - LangChain MCP: https://docs.langchain.com/oss/python/langchain/mcp
    - OpenRouter: https://openrouter.ai
"""

import os
import asyncio
from typing import Optional, List, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

# Load environment variables from .env file
load_dotenv()

# Configuration constants
OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
MCP_SERVER_URL: str = "http://localhost:9010/mcp"
MODEL_NAME: str = "deepseek/deepseek-chat-v3.1"
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
DEFAULT_TEMPERATURE: float = 0.7

# System prompt for the agent
SYSTEM_PROMPT: str = (
    "You are a helpful GIS assistant. You have access to various GIS tools "
    "through the MCP server. Use these tools to help users with geospatial "
    "operations. Always provide clear and accurate responses based on the tool results."
)


def validate_environment() -> bool:
    """
    Validate that required environment variables are set.
    
    Returns:
        bool: True if environment is valid, False otherwise.
    """
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY is not set.")
        print("Please ensure it's set in your .env file or environment variables.")
        print("Example .env file content:")
        print("  OPENROUTER_API_KEY=your_api_key_here")
        return False
    return True


def initialize_language_model() -> ChatOpenAI:
    """
    Initialize and configure the language model using OpenRouter.
    
    Returns:
        ChatOpenAI: Configured ChatOpenAI instance.
    """
    return ChatOpenAI(
        model=MODEL_NAME,
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        temperature=DEFAULT_TEMPERATURE,
    )


def initialize_mcp_client() -> MultiServerMCPClient:
    """
    Initialize the MultiServerMCPClient for connecting to the GIS MCP server.
    
    Returns:
        MultiServerMCPClient: Configured MCP client instance.
    """
    print("Initializing MCP client...")
    print(f"   Server URL: {MCP_SERVER_URL}")
    print(f"   Transport: streamable_http")
    
    client = MultiServerMCPClient(
        {
            "gis": {
                "transport": "streamable_http",
                "url": MCP_SERVER_URL,
            }
        }
    )
    print("   MCP client created successfully (lazy connection)")
    return client


async def load_gis_tools(client: MultiServerMCPClient) -> Optional[List[Any]]:
    """
    Load available GIS tools from the MCP server.
    
    Args:
        client: Initialized MultiServerMCPClient instance.
        
    Returns:
        Optional[List[Any]]: List of available tools, or None if connection fails.
    """
    print(f"\nAttempting to connect and fetch tools from {MCP_SERVER_URL}...")
    
    try:
        tools = await client.get_tools()
        
        if not tools:
            print("Warning: No tools found. Ensure the GIS MCP server is running on port 9010.")
            return None
            
        print(f"Successfully loaded {len(tools)} GIS tools!")
        return tools
        
    except Exception as e:
        print("\nError: Failed to connect to GIS MCP server!")
        print(f"   Connection URL: {MCP_SERVER_URL}")
        print("\nDiagnostics:")
        print("   1. MCP client was created successfully")
        print("   2. Connection attempt failed when calling get_tools()")
        print("   3. This indicates the server is not running or not reachable")
        print("\nTroubleshooting steps:")
        print("   1. Open a NEW terminal window (keep this one open)")
        print("   2. Activate your virtual environment:")
        print("      .\\.venv\\Scripts\\Activate.ps1  (PowerShell)")
        print("      .\\.venv\\Scripts\\activate     (CMD)")
        print("   3. Set environment variables:")
        print("      Windows PowerShell:")
        print("        $env:GIS_MCP_TRANSPORT='http'")
        print("        $env:GIS_MCP_HOST='localhost'")
        print("        $env:GIS_MCP_PORT='9010'")
        print("      Windows CMD:")
        print("        set GIS_MCP_TRANSPORT=http")
        print("        set GIS_MCP_HOST=localhost")
        print("        set GIS_MCP_PORT=9010")
        print("   4. Start the server: gis-mcp")
        print("\n   Expected server output:")
        print("      'Starting GIS MCP server with http transport on localhost:9010'")
        print("      'MCP endpoint will be available at: http://localhost:9010/mcp'")
        print("\n   Then return to this terminal and run the agent again.")
        print(f"\n   Error details: {type(e).__name__}: {str(e)}")
        return None


def extract_agent_response(result: dict) -> str:
    """
    Extract the AI response message from the agent result.
    
    Args:
        result: Result dictionary from agent invocation.
        
    Returns:
        str: The agent's response text.
    """
    messages = result.get("messages", [])
    
    # Search for AI message in reverse order (most recent first)
    for msg in reversed(messages):
        if isinstance(msg, AIMessage):
            return msg.content
    
    # Fallback to last message if no AI message found
    if messages:
        return str(messages[-1])
    
    return "No response generated"


async def run_interactive_session(agent: Any) -> None:
    """
    Run the interactive agent session loop.
    
    Args:
        agent: Initialized LangChain agent instance.
    """
    print("GIS Agent is ready. Type 'exit', 'quit', or 'q' to terminate.\n")
    
    while True:
        try:
            query = input("You: ").strip()
            
            # Check for exit commands
            if query.lower() in ["exit", "quit", "q"]:
                print("Terminating session.")
                break
            
            # Skip empty queries
            if not query:
                continue
            
            # Invoke agent with user query
            result = await agent.ainvoke({
                "messages": [{"role": "user", "content": query}]
            })
            
            # Extract and display response
            response_text = extract_agent_response(result)
            print(f"Agent: {response_text}\n")
            
        except KeyboardInterrupt:
            print("\nSession terminated by user.")
            break
        except Exception as e:
            print(f"Error during agent execution: {e}\n")


async def main() -> None:
    """
    Main entry point for the GIS agent application.
    
    Orchestrates the initialization and execution of the agent:
    1. Validates environment configuration
    2. Initializes language model
    3. Connects to GIS MCP server
    4. Loads available GIS tools
    5. Creates and runs the agent
    """
    # Validate environment
    if not validate_environment():
        return
    
    # Initialize language model
    llm = initialize_language_model()
    
    # Initialize MCP client
    client = initialize_mcp_client()
    
    # Load GIS tools from MCP server
    tools = await load_gis_tools(client)
    if tools is None:
        return
    
    # Create agent with loaded tools
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )
    
    # Run interactive session
    await run_interactive_session(agent)


if __name__ == "__main__":
    asyncio.run(main())

