import json
import os
from dataclasses import dataclass
from dataclasses import field
from typing import Any

from aiofiles import open as aio_open


@dataclass
class AuthSessions:
    enabled: bool = False


@dataclass
class StealthMode:
    enabled: bool = False


@dataclass
class IntunedSettings:
    auth_sessions: AuthSessions = field(default_factory=AuthSessions)
    stealth_mode: StealthMode = field(default_factory=StealthMode)


def default_intuned_settings() -> IntunedSettings:
    return IntunedSettings(
        auth_sessions=AuthSessions(enabled=os.environ.get("INTUNED_AUTH_SESSIONS_ENABLED", "false").lower() == "true"),
        stealth_mode=StealthMode(enabled=os.environ.get("INTUNED_STEALTH_MODE_ENABLED", "false").lower() == "true"),
    )


def validate_settings(settings_dict: dict[Any, Any]) -> IntunedSettings:
    auth_sessions = AuthSessions(
        enabled=settings_dict.get("authSessions", {}).get(
            "enabled", os.environ.get("INTUNED_AUTH_SESSIONS_ENABLED", "false").lower() == "true"
        )
    )
    stealth_mode = StealthMode(
        enabled=settings_dict.get("stealthMode", {}).get(
            "enabled", os.environ.get("INTUNED_STEALTH_MODE_ENABLED", "false").lower() == "true"
        )
    )
    return IntunedSettings(auth_sessions=auth_sessions, stealth_mode=stealth_mode)


def load_intuned_settings_sync() -> IntunedSettings:
    settings_path = os.path.join(os.getcwd(), "Intuned.json")
    if not os.path.exists(settings_path):
        return default_intuned_settings()
    try:
        with open(settings_path) as settings_file:
            content = settings_file.read()
            settings_dict = json.loads(content)
        return validate_settings(settings_dict)
    except json.JSONDecodeError as e:
        raise Exception("Invalid Intuned.json file") from e


async def load_intuned_settings() -> IntunedSettings:
    settings_path = os.path.join(os.getcwd(), "Intuned.json")
    if not os.path.exists(settings_path):
        return default_intuned_settings()
    try:
        async with aio_open(settings_path) as settings_file:
            content = await settings_file.read()
            settings_dict = json.loads(content)
        return validate_settings(settings_dict)
    except json.JSONDecodeError as e:
        raise Exception("Invalid Intuned.json file") from e
