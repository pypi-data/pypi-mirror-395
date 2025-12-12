from typing import Any, Dict, List, Optional

from sayou.core.base_component import BaseComponent
from sayou.core.decorators import safe_run

from .core.exceptions import WriterError
from .interfaces.base_writer import BaseWriter
from .writer.console_writer import ConsoleWriter
from .writer.file_writer import FileWriter
from .writer.jsonl_writer import JsonLineWriter


class LoaderPipeline(BaseComponent):
    """
    Orchestrates the data loading process.

    Acts as a router that dispatches the data payload to the appropriate
    writer implementation based on the `strategy` key (e.g., 'file', 'neo4j').
    """

    component_name = "LoaderPipeline"

    def __init__(self, extra_writers: Optional[List[BaseWriter]] = None):
        """
        Initialize all registered writers.
        Passes global configuration (e.g., DB connection pools) to writers.
        """
        super().__init__()
        self.writers: Dict[str, BaseWriter] = {}

        defaults = [FileWriter(), JsonLineWriter(), ConsoleWriter()]
        self._register(defaults)

        if extra_writers:
            self._register(extra_writers)

    def _register(self, writers: List[BaseWriter]):
        for w in writers:
            for t in getattr(w, "SUPPORTED_TYPES", []):
                self.writers[t] = w

    @safe_run(default_return=None)
    def initialize(self, **kwargs):
        for w in set(self.writers.values()):
            if hasattr(w, "initialize"):
                w.initialize(**kwargs)
        self._log(f"LoaderPipeline initialized. Writers: {list(self.writers.keys())}")

    def run(
        self, data: Any, destination: str, strategy: str = "file", **kwargs
    ) -> bool:
        """
        Execute the loading strategy.

        Args:
            data (Any): The payload to write.
            destination (str): Target location/URI.
            strategy (str): The writer strategy to use (default: 'file').
            **kwargs: Additional writer-specific options (auth, mode).

        Returns:
            bool: True if operation was successful.

        Raises:
            WriterError: If the strategy is unknown or writing fails.
        """
        writer = self.writers.get(strategy)
        if not writer:
            raise WriterError(
                f"Unknown strategy '{strategy}'. Available: {list(self.writers.keys())}"
            )

        self._log(f"Loading using strategy: {strategy}")
        return writer.write(data, destination, **kwargs)
