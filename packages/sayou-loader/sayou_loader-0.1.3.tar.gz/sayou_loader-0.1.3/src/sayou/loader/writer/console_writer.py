import json
from typing import Any

from ..interfaces.base_writer import BaseWriter


class ConsoleWriter(BaseWriter):
    """
    (Tier 2) Prints data to stdout. Useful for debugging pipelines.
    """

    component_name = "ConsoleWriter"
    SUPPORTED_TYPES = ["console", "stdout", "print"]

    def _do_write(self, data: Any, destination: str, **kwargs) -> bool:
        print(f"\n--- [ConsoleWriter] Output to: {destination} ---")

        if isinstance(data, (dict, list)):
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(data)

        print("----------------------------------------------\n")
        return True
