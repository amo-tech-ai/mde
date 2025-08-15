"""
Flight Search Agent Module

This module implements an AI-powered flight search system using LangGraph.
It creates a React agent specialized in searching for flights and booking info.
"""

from datetime import datetime

from blaxel.langgraph import bl_model, bl_tools
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


async def agent():
    """
    Main flight search agent function that creates a LangGraph React agent.

    Returns:
        A LangGraph React agent configured for flight searches

    This function:
    1. Sets up the necessary tools and models
    2. Creates a React agent with flight search capabilities
    3. Returns the configured agent
    """
    # Initialize tools and model for the agent
    tools = await bl_tools(["explorer-mcp"])
    model = await bl_model("sandbox-openai")

    # Create a comprehensive prompt for the flight search agent
    prompt = """You are an expert flight search assistant specializing in finding
the best flight options.

Your primary responsibilities:
1. Search for flights based on user criteria (departure, destination, dates)
2. Analyze multiple flight options and compare them
3. Find and present booking providers for each flight
4. Provide detailed information including:
   - Airlines and flight numbers
   - Departure and arrival times
   - Flight duration
   - Prices
   - Direct booking links
   - Available booking providers

When searching for flights:
- Use the current year ({current_year}) if no year is specified
- Search for at least 5 flight options when possible
- Include both direct and connecting flights if relevant
- Consider factors like price, duration, and convenience
- Load individual flight pages to find all available booking providers

Output format:
Present your findings in a clear, organized manner with:
- A summary of the search criteria
- Top 5-10 flight recommendations ranked by value
- For each flight, include all relevant details and booking links
- Highlight best options based on different priorities (price, speed, convenience)

Remember to be helpful, thorough, and provide actionable booking information.""".format(
        current_year=datetime.now().year
    )

    return create_react_agent(
        name="flight-agent",
        model=model,
        tools=tools,
        prompt=prompt,
        checkpointer=MemorySaver(),
    )
