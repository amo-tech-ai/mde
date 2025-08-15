from logging import getLogger

from blaxel.langgraph import bl_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph_supervisor import create_supervisor

from .flight import agent as flight_agent
from .hotel import agent as hotel_agent

logger = getLogger(__name__)


async def agent():
    model = await bl_model("sandbox-openai")

    # Both flight and hotel agents are now LangGraph agents
    flight = await flight_agent()
    hotel = await hotel_agent()

    supervisor_graph = create_supervisor(
        [flight, hotel],
        model=model,
        supervisor_name="supervisor-agent",
        prompt="""
        You are a supervisor agent that can delegate tasks to other agents.
        You specialize in booking trips. You have access to these agents:
        - flight-agent: Search and book flights
        - hotel-agent: Search and book hotels

        You can delegate tasks to both agents if you feel it is necessary.
        Analyze the user's request and route it to the appropriate agent(s).
        """,
    )

    agent = supervisor_graph.compile(
        name="supervisor-agent", checkpointer=MemorySaver()
    )
    return agent
