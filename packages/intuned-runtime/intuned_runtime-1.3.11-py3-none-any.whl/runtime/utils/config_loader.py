from anyio import Path
from pydantic import TypeAdapter

from runtime.types import IntunedJson


async def load_intuned_json() -> IntunedJson | None:
    """
    Load the Intuned.json configuration file.
    Returns None if file doesn't exist or fails to parse.
    """
    intuned_json_path = Path("Intuned.json")
    if not await intuned_json_path.exists():
        return None
    try:
        return TypeAdapter[IntunedJson](IntunedJson).validate_json(await intuned_json_path.read_text())
    except Exception:
        return None
