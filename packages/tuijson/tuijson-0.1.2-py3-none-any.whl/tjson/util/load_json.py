import json
import sys
from pathlib import Path
from typing import Any


def load_json_input(arg: str) -> tuple[dict[str, Any], str]:
    """Parses the argument as a file path or raw JSON string."""
    # 1. Try treating it as a file path
    path = Path(arg)

    if path.exists() and path.is_file():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f), path.name
        except json.JSONDecodeError as e:
            sys.exit(f"Error decoding JSON file: {e}")

    # 2. Try treating it as a raw JSON string
    try:
        return json.loads(arg), "Raw String"
    except json.JSONDecodeError:
        sys.exit(f"Error: Argument is neither a valid file path nor valid JSON string.\nInput: {arg[:50]}...")
