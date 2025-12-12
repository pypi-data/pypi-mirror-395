from typing import Any, Dict, List, Optional

from sayou.core.base_component import BaseComponent
from sayou.core.decorators import safe_run

from .builder.graph_builder import GraphBuilder
from .builder.vector_builder import VectorBuilder
from .core.exceptions import BuildError
from .interfaces.base_builder import BaseBuilder


class AssemblerPipeline(BaseComponent):
    """
    Orchestrates the assembly process.

    This pipeline acts as a factory, routing standardized `SayouOutput` (Nodes)
    to specific builders to generate database-ready payloads (Graph Dicts,
    Vector Lists, or Query Strings).
    """

    component_name = "AssemblerPipeline"

    def __init__(self, extra_builders: Optional[List[BaseBuilder]] = None):
        """
        Initialize the pipeline with default and custom builders.

        Args:
            extra_builders (List[BaseBuilder], optional): Custom builders to register.
        """
        super().__init__()
        self.builders: Dict[str, BaseBuilder] = {}

        defaults = [GraphBuilder(), VectorBuilder()]
        self._register(defaults)

        if extra_builders:
            self._register(extra_builders)

    def _register(self, builders: List[BaseBuilder]):
        """
        Register builders into the internal strategy map.

        Args:
            builders (List[BaseBuilder]): Builder instances to register.
        """
        for b in builders:
            for t in getattr(b, "SUPPORTED_TYPES", []):
                self.builders[t] = b

    @safe_run(default_return=None)
    def initialize(self, **kwargs):
        """
        Initialize all registered builders.

        Passes global configuration (e.g., embedding functions) to builders.
        """
        for b in set(self.builders.values()):
            if hasattr(b, "initialize"):
                b.initialize(**kwargs)
        self._log(
            f"AssemblerPipeline initialized. Strategies: {list(self.builders.keys())}"
        )

    def run(self, input_data: Any, strategy: str = "graph") -> Any:
        """
        Execute the assembly strategy.

        Args:
            input_data (Any): WrapperOutput object or Dictionary.
            strategy (str): The building strategy (default: 'graph').

        Returns:
            Any: The assembled payload (Dict, List, or Str) ready for Loader.

        Raises:
            BuildError: If the strategy is unknown or execution fails.
        """
        builder = self.builders.get(strategy)
        if not builder:
            raise BuildError(
                f"Unknown strategy '{strategy}'. Available: {list(self.builders.keys())}"
            )

        self._log(f"Assembling using strategy: {strategy}")
        return builder.build(input_data)
