from typing import List, Dict, Optional, Any
from arctic_orchestra.Tools.agent_2_tool import Agent2Tool
from arctic_orchestra.Agents.base import Agent


class RoutingOrchestrator:
    """
    High-level orchestrator that converts multiple specialized Agents
    into callable tools, enforces an execution sequence, and builds a 
    RouterAgent responsible for end-to-end reasoning and routing.

    Responsibilities:
    - Accept an array of agents in the desired execution order.
    - Wrap each agent as a tool using Agent2Tool.
    - Inject optional per-agent routing prompts (constraints, order logic, etc.).
    - Create a master RouterAgent that calls these tools in sequence, passing
      outputs forward automatically.
    
    Users may supply `additional_routing_instructions` to customize 
    sequencing rules, constraints, or workflow logic.
    """

    BASE_ROUTING_CONTRACT = """
    You are a Routing Orchestrator.

    Your job is:
    1. To analyze the user's raw request.
    2. To call the wrapped agent-tools in the correct sequence.
    3. After each tool call, take its **output** and feed it into the next tool directly or by modifying it to its need.
    4. Make sure the input to the agents are tailered to its needs donot feed references of other agents or task that deosnot relate to the tool.
    5. Continue until all tools have run OR until the task is complete.
    6. Produce the final combined result only after running the last tool.
    """

    def __init__(
        self,
        model,
        agents: List[Any],
        additional_routing_instructions: Optional[str] = None,
        max_iteration: int = 10,
        debug: bool = False

    ):
        """
        :param model: The LLM client (must expose .run).
        :param agents: Ordered list of Agent instances.
        :param additional_routing_instructions: Optional user-defined routing logic.
        """
        self.model = model
        self.agents = agents
        self.additional_routing_instructions = additional_routing_instructions or ""
        self.router_tools: Dict[str, Any] = {}
        self.max_iteration = max_iteration
        self.debug = debug


    def wrap_agents_as_tools(self):
        """
        Converts each agent into a tool using Agent2Tool.
        Preserves order of the agent list.
        """
        for agent in self.agents:
            tool_name, tool_func = Agent2Tool(
                agent,
                additional_prompt=f"This tool represents: {agent.name}. "
                                  f"Use it only for its specialized purpose."
            ).create_tool()

            self.router_tools[tool_name] = tool_func

        return self.router_tools

    def build_router_agent(self, name: str = "RouterAgent"):
        """
        Constructs the final RouterAgent responsible for orchestrating
        all agent-tools in the given order.
        """
        # Step 1 — wrap agents
        router_tools = self.wrap_agents_as_tools()

        # Step 2 — create the final routing instructions
        ordered_tool_list = list(router_tools.keys())

        ordered_instructions = "\n".join(
            [f"{i+1}. Call **{tool_name}**" for i, tool_name in enumerate(ordered_tool_list)]
        )

        routing_prompt = (
            self.BASE_ROUTING_CONTRACT
            + "\nExecution Order:\n"
            + ordered_instructions
            + "\n\nUser Additional Instructions:\n"
            + self.additional_routing_instructions
        )

        # Step 3 — construct Router Agent
        router_agent = Agent(
            model=self.model,
            name=name,
            identity="You are the master router coordinating specialized agents.",
            instruction=routing_prompt,
            task="Route the user request through all tools in sequence.",
            tools=router_tools,
            max_iterations=self.max_iteration,
            debug=self.debug
        )

        return router_agent
