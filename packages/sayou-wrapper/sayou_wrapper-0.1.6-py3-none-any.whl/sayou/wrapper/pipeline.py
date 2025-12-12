from typing import Any, Dict, List, Optional

from sayou.core.base_component import BaseComponent
from sayou.core.decorators import safe_run
from sayou.core.schemas import SayouOutput

from .adapter.document_chunk_adapter import DocumentChunkAdapter
from .core.exceptions import AdaptationError
from .interfaces.base_adapter import BaseAdapter


class WrapperPipeline(BaseComponent):
    """
    Orchestrates the data wrapping process.

    This pipeline acts as the final gateway before data storage. It receives
    processed data (usually chunks) and delegates it to a specific `Adapter`
    to convert it into the standard `SayouNode` format.
    """

    component_name = "WrapperPipeline"

    def __init__(self, extra_adapters: Optional[List[BaseAdapter]] = None):
        """
        Initialize the pipeline with default and optional custom adapters.

        Args:
            extra_adapters (List[BaseAdapter], optional): Custom adapters to register.
        """
        super().__init__()
        self.adapters: Dict[str, BaseAdapter] = {}

        defaults = [DocumentChunkAdapter()]
        self._register(defaults)

        if extra_adapters:
            self._register(extra_adapters)

    def _register(self, adapters: List[BaseAdapter]):
        """
        Register a list of adapters into the internal strategy map.

        Args:
            adapters (List[BaseAdapter]): Adapter instances to register.
        """
        for a in adapters:
            for t in getattr(a, "SUPPORTED_TYPES", []):
                self.adapters[t] = a

    @safe_run(default_return=None)
    def initialize(self, **kwargs):
        """
        Initialize all registered adapters.

        Propagates global configuration to all adapters, although adapters
        are typically stateless.
        """
        for adapter in set(self.adapters.values()):
            if hasattr(adapter, "initialize"):
                adapter.initialize(**kwargs)
        self._log(
            f"WrapperPipeline initialized. Strategies: {list(self.adapters.keys())}"
        )

    def run(self, input_data: Any, strategy: str = "default") -> SayouOutput:
        """
        Execute the wrapping strategy.

        Args:
            input_data (Any): The input data (e.g., List[Chunk] or raw Dict).
            strategy (str): The adapter strategy to use (default: 'default').

        Returns:
            SayouOutput: A container holding the list of standardized SayouNodes.

        Raises:
            AdaptationError: If the strategy is unknown or execution fails.
        """
        adapter = self.adapters.get(strategy)
        if not adapter:
            raise AdaptationError(
                f"Unknown strategy '{strategy}'. Available: {list(self.adapters.keys())}"
            )

        self._log(f"Wrapping using strategy: {strategy}")
        return adapter.adapt(input_data)
