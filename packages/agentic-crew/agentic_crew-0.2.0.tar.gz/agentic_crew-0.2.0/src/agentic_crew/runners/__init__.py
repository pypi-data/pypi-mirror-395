"""Framework-specific runners for agentic-crew.

Each runner implements the same interface but targets a different AI framework:
- CrewAIRunner: Full-featured, best for complex crews
- LangGraphRunner: Graph-based flows, good for conditional logic
- StrandsRunner: Lightweight, AWS-native

Usage:
    from agentic_crew.runners import get_runner

    runner = get_runner("crewai")  # Or "langgraph", "strands", "auto"
    crew = runner.build_crew(config)
    result = runner.run(crew, inputs)
"""

from agentic_crew.core.decomposer import get_runner

__all__ = ["get_runner"]
