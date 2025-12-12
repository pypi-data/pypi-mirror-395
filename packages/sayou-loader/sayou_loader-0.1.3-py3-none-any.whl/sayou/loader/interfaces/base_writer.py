from abc import abstractmethod
from typing import Any

from sayou.core.base_component import BaseComponent
from sayou.core.decorators import measure_time, retry

from ..core.exceptions import WriterError


class BaseWriter(BaseComponent):
    """
    (Tier 1) Abstract base class for data writers (Loaders).

    Implements the Template Method pattern with built-in retries and logging.
    """

    component_name = "BaseWriter"
    SUPPORTED_TYPES = []

    @measure_time
    @retry(max_retries=3, delay=1.0)
    def write(self, data: Any, destination: str, **kwargs) -> bool:
        """
        [Template Method] Execute the write operation.

        Args:
            data (Any): The payload to write (from Assembler).
            destination (str): Target location (File path, DB connection string, Table name).
            **kwargs: Additional options (mode, encoding, etc.).

        Returns:
            bool: True if successful.

        Raises:
            WriterError: If writing fails after retries.
        """
        self._log(f"Writing to '{destination}' (Type: {type(data).__name__})")

        if not data:
            self._log("Data is empty. Skipping write.", level="warning")
            return False

        try:
            result = self._do_write(data, destination, **kwargs)
            if result:
                self._log("Write completed successfully.")
            else:
                self._log("Write completed but returned False.", level="warning")
            return result

        except Exception as e:
            wrapped_error = WriterError(f"[{self.component_name}] Failed: {str(e)}")
            self.logger.error(wrapped_error, exc_info=True)
            raise wrapped_error

    @abstractmethod
    def _do_write(self, data: Any, destination: str, **kwargs) -> bool:
        """
        [Abstract Hook] Implement the actual I/O logic.
        """
        raise NotImplementedError
