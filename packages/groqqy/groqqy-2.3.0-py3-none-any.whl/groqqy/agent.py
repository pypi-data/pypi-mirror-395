"""
Agent - Agentic loop implementation

Implements: Think → Act → Observe pattern
Enables multi-step reasoning and tool chaining
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from .provider import Provider
from .tool import ToolRegistry
from .components import ConversationManager, ToolExecutor, CostTracker
from .log import get_logger
from .strategy import ToolExecutionStrategy, detect_strategy


@dataclass
class AgentResult:
    """
    Result from agent execution.

    Contains final response plus metadata about the execution.
    """
    response: str
    iterations: int
    total_cost: float
    tool_calls_made: int
    conversation: List[Dict[str, Any]]


class Agent:
    """
    Agentic loop: Think → Act → Observe → Repeat.

    The agent can:
    - Make multiple LLM calls
    - Use tools multiple times
    - Chain tool calls together
    - Reason over tool results

    This enables true agentic behavior beyond simple single-turn chat.
    """

    def __init__(
        self,
        provider: Provider,
        tools: ToolRegistry,
        max_iterations: int = 10,
        logger=None,
        strategy: Optional[ToolExecutionStrategy] = None
    ):
        """
        Initialize agent.

        Args:
            provider: LLM provider (e.g., GroqProvider)
            tools: ToolRegistry with available tools
            max_iterations: Maximum agent loop iterations (prevents infinite loops)
            logger: Optional logger
            strategy: Tool execution strategy (auto-detected if not provided)
        """
        self.provider = provider
        self.tools = tools
        self.max_iterations = max_iterations
        self.log = logger or get_logger("agent")

        # Auto-detect strategy based on tool types (or use default if no tools)
        if tools is not None:
            self.strategy = strategy or detect_strategy(tools.to_schemas())
        else:
            # No tools - strategy won't be used, but we need a valid object
            from .strategy import LocalToolStrategy
            self.strategy = LocalToolStrategy()

        self.log.debug(f"Agent initialized with {self.strategy.describe()}")

        # Components (composable!)
        self.conversation = ConversationManager()
        self.executor = ToolExecutor(tools, logger) if tools is not None else None
        self.tracker = CostTracker()

    def run(self, prompt: str) -> AgentResult:
        """
        Run the agent loop until task is complete.

        Flow:
        1. Add user prompt to conversation
        2. Loop:
           a. THINK: Get LLM response
           b. ACT: Execute any tool calls
           c. OBSERVE: Add results to conversation
           d. Repeat until LLM returns without tool calls
        3. Return final response

        Args:
            prompt: User's input message

        Returns:
            AgentResult with response and execution metadata
        """
        self.conversation.add_user(prompt)
        iteration = 0
        tool_calls_made = 0

        self.log.debug("Agent run started",
                      prompt_length=len(prompt),
                      max_iterations=self.max_iterations)

        while iteration < self.max_iterations:
            iteration += 1
            self.log.debug(f"Agent iteration {iteration}/{self.max_iterations}")

            # THINK: What should I do next?
            response = self._call_llm()

            # Track cost
            cost = self.provider.get_cost(response.usage)
            self.tracker.add(cost, {"iteration": iteration})

            # ACT: Let strategy decide how to handle response
            tools_schemas = self.tools.to_schemas() if self.tools is not None else []
            execution_result = self.strategy.handle_response(
                response,
                tools_schemas
            )

            if execution_result.needs_continuation:
                # Strategy says we need to execute tools locally
                num_tools = len(execution_result.tool_calls)
                tool_calls_made += num_tools

                # Show what tools are about to be executed
                tool_summaries = []
                for tc in execution_result.tool_calls:
                    name = tc['function']['name']
                    args = tc['function']['arguments']
                    # Parse args to show command if it's run_command
                    try:
                        import json
                        args_dict = json.loads(args) if isinstance(args, str) else args
                        if name == "run_command" and "command" in args_dict:
                            tool_summaries.append(f"{name}('{args_dict['command']}')")
                        else:
                            tool_summaries.append(name)
                    except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
                        tool_summaries.append(name)

                self.log.info(f"Executing {num_tools} tool(s)",
                             iteration=iteration,
                             tools=tool_summaries)

                # Add tool calls to conversation
                self.conversation.add_tool_calls(
                    response.text, execution_result.tool_calls
                )

                # Execute all tools
                for tool_call in execution_result.tool_calls:
                    # OBSERVE: Get tool result
                    result = self.executor.execute(tool_call)

                    # Add result to conversation (LLM will see this next iteration)
                    self.conversation.add_tool_result(tool_call['id'], result)

                # Continue loop - LLM will process tool results
                continue

            # Strategy says we're done (no local execution needed)
            self.conversation.add_assistant(response.text)

            # DEBUG: Log what we're returning
            final_response = execution_result.content or response.text
            exec_content = (
                execution_result.content[:100]
                if execution_result.content else None
            )
            resp_text = response.text[:100] if response.text else None
            final_resp = final_response[:100] if final_response else None
            self.log.info("Agent run completed",
                         iterations=iteration,
                         tool_calls_made=tool_calls_made,
                         total_cost=self.tracker.get_total(),
                         execution_result_content=exec_content,
                         response_text=resp_text,
                         final_response=final_resp)

            return AgentResult(
                response=final_response,
                iterations=iteration,
                total_cost=self.tracker.get_total(),
                tool_calls_made=tool_calls_made,
                conversation=self.conversation.get_history()
            )

        # Max iterations reached - return partial result
        self.log.warning(f"Max iterations ({self.max_iterations}) reached",
                        tool_calls_made=tool_calls_made)

        return AgentResult(
            response="[Agent reached max iterations - task may be incomplete]",
            iterations=iteration,
            total_cost=self.tracker.get_total(),
            tool_calls_made=tool_calls_made,
            conversation=self.conversation.get_history()
        )

    def _call_llm(self):
        """
        Call LLM with current conversation and available tools.

        Returns:
            LLMResponse from provider
        """
        # Pass None for tools if no tool registry
        tools_schemas = self.tools.to_schemas() if self.tools is not None else None
        return self.provider.chat(
            messages=self.conversation.get_history(),
            tools=tools_schemas
        )

    def reset(self):
        """Reset agent state (conversation, costs)."""
        self.conversation.reset()
        self.tracker.reset()
        self.log.debug("Agent reset")
