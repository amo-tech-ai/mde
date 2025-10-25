from blaxel.langgraph import bl_model, bl_tools
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


async def agent():
    """
    Main hotel search agent function that creates a LangGraph React agent.
    
    Returns:
        A LangGraph React agent configured for hotel searches
    """
    tools = await bl_tools(["explorer-mcp"])
    model = await bl_model("sandbox-openai")
    
    prompt = """You are an expert hotel search assistant specializing in finding
the best hotel options for travelers.

Your primary responsibilities:
1. Search for hotels based on user criteria (location, dates, budget, preferences)
2. Analyze multiple hotel options and compare them
3. Find and present booking providers for each hotel
4. Provide detailed information including:
   - Hotel name and location
   - Star rating and amenities
   - Room types and pricing
   - Cancellation policies
   - Guest reviews and ratings
   - Direct booking links
   - Available booking providers

When searching for hotels:
- Consider factors like price, location, ratings, and amenities
- Search for at least 5-10 hotel options when possible
- Include hotels across different price ranges
- Load individual hotel pages to find all available booking providers
- Check for special offers or deals

Output format:
Present your findings in a clear, organized manner with:
- A summary of the search criteria
- Top 5-10 hotel recommendations ranked by value
- For each hotel, include all relevant details and booking links
- Highlight best options based on different priorities (price, luxury, location)

Remember to be helpful, thorough, and provide actionable booking information."""
    
    return create_react_agent(
        name="hotel-agent",
        model=model,
        tools=tools,
        prompt=prompt,
        checkpointer=MemorySaver(),
    )
