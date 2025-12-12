import json
import os
from typing import Any

from ..interfaces.base_writer import BaseWriter


class JsonLineWriter(BaseWriter):
    """
    Writes a list of dictionaries to a JSONL file.

    Useful for large datasets like logs or vector embeddings where
    loading the entire file into memory is inefficient.
    """

    component_name = "JsonLineWriter"
    SUPPORTED_TYPES = ["jsonl", "stream"]

    def _do_write(self, data: Any, destination: str, **kwargs) -> bool:
        """
        Iterate through the list and write each item as a JSON line.
        """
        if not isinstance(data, list):
            self._log("JsonLineWriter expects a list of data.", level="warning")
            return False

        folder = os.path.dirname(destination)
        if folder:
            os.makedirs(folder, exist_ok=True)

        mode = kwargs.get("mode", "w")

        with open(destination, mode, encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        return True
