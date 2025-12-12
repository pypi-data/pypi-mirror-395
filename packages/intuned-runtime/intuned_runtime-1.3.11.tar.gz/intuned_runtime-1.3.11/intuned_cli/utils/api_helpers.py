import json
from typing import Any
from typing import Callable
from typing import get_args
from typing import Literal
from typing import overload

import toml
import yaml
from anyio import Path
from jsonc_parser.parser import JsoncParser  # type: ignore
from pydantic import BaseModel
from pydantic import TypeAdapter

from intuned_cli.utils.error import CLIError
from runtime.types import IntunedJson


@overload
async def assert_api_file_exists(dirname: Literal["api"], api_name: str) -> None: ...
@overload
async def assert_api_file_exists(dirname: Literal["auth-sessions"], api_name: Literal["create", "check"]) -> None: ...


async def assert_api_file_exists(dirname: Literal["api", "auth-sessions"], api_name: str) -> None:
    """
    Assert that the API file exists in the specified folder.
    """
    path = (await Path().resolve()) / dirname / f"{api_name}.py"
    if not await path.exists():
        raise CLIError("File does not exist")


async def load_intuned_json() -> IntunedJson:
    intuned_settings_file = await get_intuned_settings_file()

    intuned_settings_content = await Path(intuned_settings_file.file_path).read_text()

    parsed_content = intuned_settings_file.parse(intuned_settings_content)

    try:
        return TypeAdapter[IntunedJson](IntunedJson).validate_python(parsed_content)
    except Exception as e:
        raise CLIError(f"Failed to parse {intuned_settings_file.name}: {e}") from e


IntunedSettingsFileName = Literal["Intuned.json", "Intuned.jsonc", "Intuned.yaml", "Intuned.yml", "Intuned.toml"]

intuned_file_names: list[IntunedSettingsFileName] = list(get_args(IntunedSettingsFileName))


class IntunedSettingsFile(BaseModel):
    name: IntunedSettingsFileName
    file_path: str
    parse: Callable[[str], Any]


intuned_settings_parsers: dict[IntunedSettingsFileName, Callable[[str], Any]] = {
    "Intuned.json": json.loads,
    "Intuned.jsonc": lambda content: JsoncParser.parse_str(content),  # type: ignore
    "Intuned.yaml": yaml.safe_load,
    "Intuned.yml": yaml.safe_load,
    "Intuned.toml": toml.loads,
}


async def get_intuned_settings_file() -> IntunedSettingsFile:
    for file_name in intuned_file_names:
        path = Path(file_name)
        if await path.exists():
            return IntunedSettingsFile(
                name=file_name,
                file_path=str(path),
                parse=intuned_settings_parsers[file_name],
            )
    raise CLIError(
        "No Intuned settings file found in the current directory. Expected one of: " + ", ".join(intuned_file_names)
    )


async def get_intuned_settings_file_name() -> str:
    return (await get_intuned_settings_file()).name
