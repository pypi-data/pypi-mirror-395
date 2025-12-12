import json
import os
import pickle
from typing import Any

from ..interfaces.base_writer import BaseWriter


class FileWriter(BaseWriter):
    """
    Writes data to the local file system.

    Automatically handles format serialization:
    - Dict/List -> JSON
    - Str -> Text file
    - Bytes -> Binary file
    - Others -> Pickle
    """

    component_name = "FileWriter"
    SUPPORTED_TYPES = ["file", "local", "json"]

    def _do_write(self, data: Any, destination: str, **kwargs) -> bool:
        """
        Write data to file. Creates parent directories if they don't exist.
        """
        # 1. Handle Directory Destination
        if os.path.isdir(destination):
            destination = os.path.join(destination, "output.json")
            self._log(f"Destination is a directory. Appended filename: {destination}")

        # 2. Create Parent Directory
        folder = os.path.dirname(destination)
        if folder:
            os.makedirs(folder, exist_ok=True)

        mode = kwargs.get("mode", "w")
        encoding = kwargs.get("encoding", "utf-8")

        # 3. Determine Content & Mode
        if isinstance(data, (dict, list)):
            content = json.dumps(data, indent=2, ensure_ascii=False)
        elif isinstance(data, str):
            content = data
        elif isinstance(data, bytes):
            content = data
            mode = "wb"
            encoding = None
        else:
            # Fallback: Pickle
            with open(destination + ".pkl", "wb") as f:
                pickle.dump(data, f)
            return True

        # 4. Write File
        with open(destination, mode, encoding=encoding) as f:
            f.write(content)

        return True
