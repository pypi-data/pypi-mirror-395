"""Base runner interface for framework-specific implementations.

All runners must implement this interface to ensure consistent behavior
across CrewAI, LangGraph, and Strands.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseRunner(ABC):
    """Abstract base class for framework runners.

    Each framework runner converts agentic-crew's universal crew format
    into framework-specific objects and executes them.
    """

    framework_name: str = "base"

    @abstractmethod
    def build_crew(self, crew_config: dict[str, Any]) -> Any:
        """Build a framework-specific crew from configuration.

        Args:
            crew_config: Universal crew configuration dict containing:
                - name: Crew name
                - description: What the crew does
                - agents: Dict of agent configs
                - tasks: Dict of task configs
                - knowledge_paths: List of knowledge directory paths

        Returns:
            Framework-specific crew object (Crew, Graph, Agent, etc.)
        """
        pass

    @abstractmethod
    def run(self, crew: Any, inputs: dict[str, Any]) -> str:
        """Execute the crew with inputs.

        Args:
            crew: Framework-specific crew object from build_crew().
            inputs: Input dict to pass to the crew.

        Returns:
            Crew output as a string.
        """
        pass

    def build_and_run(
        self,
        crew_config: dict[str, Any],
        inputs: dict[str, Any] | None = None,
    ) -> str:
        """Convenience method to build and run in one step.

        Args:
            crew_config: Crew configuration.
            inputs: Optional inputs for the crew.

        Returns:
            Crew output as string.
        """
        crew = self.build_crew(crew_config)
        return self.run(crew, inputs or {})

    @abstractmethod
    def build_agent(self, agent_config: dict[str, Any], tools: list | None = None) -> Any:
        """Build a framework-specific agent.

        Args:
            agent_config: Agent configuration with role, goal, backstory.
            tools: Optional list of tools to give the agent.

        Returns:
            Framework-specific agent object.
        """
        pass

    @abstractmethod
    def build_task(self, task_config: dict[str, Any], agent: Any) -> Any:
        """Build a framework-specific task.

        Args:
            task_config: Task configuration with description, expected_output.
            agent: Agent to assign to the task.

        Returns:
            Framework-specific task object.
        """
        pass

    def get_llm(self, model: str | None = None) -> Any:
        """Get the LLM for this framework.

        Args:
            model: Optional model name override. If None, uses DEFAULT_MODEL.

        Returns:
            Framework-specific LLM object.
        """
        # Default implementation - subclasses can override
        # Import lazily to avoid requiring crewai at module load time
        try:
            from agentic_crew.config.llm import DEFAULT_MODEL, get_llm

            # Use default model if none specified to avoid AttributeError
            return get_llm(model if model else DEFAULT_MODEL)
        except ImportError:
            # If llm module not available, return None (framework may have its own default)
            return None
