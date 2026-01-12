from pathlib import Path
import json
from typing import Any, Union

DEFAULT_JSON_INDENT = 2


def log_to_file(
    path: Union[str, Path],
    content: Any,
    *,
    as_json: bool = False,
    mode: str = "w",
    encoding: str = "utf-8",
) -> Path:
    """
    Write content to a file, creating parent folders if needed.

    Args:
        path: File path (str or Path)
        content: Data to write
        as_json: Dump content as JSON
        mode: "w" (overwrite) or "a" (append)
        encoding: File encoding

    Returns:
        Path to the written file
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(mode, encoding=encoding) as f:
        if as_json:
            json.dump(content, f, indent=DEFAULT_JSON_INDENT, ensure_ascii=False)
        else:
            f.write(str(content))

    return path
