import base64
import json
import logging
import os
from pathlib import Path
from typing import Any

from playwright.async_api import BrowserContext

from runtime.browser.extensions.intuned_extension_server import setup_intuned_extension_server
from runtime.context.context import IntunedContext
from runtime.env import get_functions_domain
from runtime.env import get_project_id
from runtime.env import get_workspace_id
from runtime.types import CaptchaSolverSettings
from runtime.types.settings_types import CaptchaSolverApiKeyAuthentication
from runtime.types.settings_types import CaptchaSolverTokenSettings
from runtime.utils.config_loader import load_intuned_json

logger = logging.getLogger(__name__)

captcha_settings: CaptchaSolverSettings | None = None


def get_intuned_extension_path() -> Path | None:
    if "INTUNED_EXTENSION_PATH" not in os.environ:
        return None
    intuned_extension_path = Path(os.environ["INTUNED_EXTENSION_PATH"])
    if not intuned_extension_path.exists():
        return None
    return intuned_extension_path


def is_intuned_extension_loaded() -> bool:
    return "INTUNED_EXTENSION_PATH" in os.environ


async def is_intuned_extension_enabled() -> bool:
    intuned_extension_path = get_intuned_extension_path()
    if intuned_extension_path is None:
        return False

    captcha_solver = await get_intuned_captcha_solver_settings()

    return captcha_solver.enabled


async def get_intuned_worker(context: BrowserContext):
    if not is_intuned_extension_loaded():
        return None

    for attempt in range(5):
        for service_worker in context.service_workers:
            if "intunedWorker.js" in service_worker.url:
                return service_worker
        try:
            if attempt < 4:
                await context.wait_for_event("serviceworker", timeout=3000)
        except Exception as e:
            logger.warning(f"Error accessing service workers (attempt {attempt + 1}): {e}")

    logger.warning("Failed to get intuned worker after 5 attempts")
    return None


def get_intuned_extension_authentication() -> CaptchaSolverApiKeyAuthentication | CaptchaSolverTokenSettings:
    if "INTUNED_API_KEY" in os.environ:
        api_key = os.environ["INTUNED_API_KEY"]
        return CaptchaSolverApiKeyAuthentication(type="apiKey", apiKey=api_key)
    if "INTUNED_BASIC_AUTH_USERNAME" in os.environ and "INTUNED_BASIC_AUTH_PASSWORD" in os.environ:
        username = os.environ["INTUNED_BASIC_AUTH_USERNAME"]
        password = os.environ["INTUNED_BASIC_AUTH_PASSWORD"]
        credentials = f"{username}:{password}"
        token = base64.b64encode(credentials.encode()).decode()
        return CaptchaSolverTokenSettings(type="basic", token=token)
    context = IntunedContext.current()
    return CaptchaSolverTokenSettings(type="bearer", token=context.functions_token)


def get_intuned_base_url() -> str | None:
    if "INTUNED_API_BASE_URL" in os.environ:
        return os.environ["INTUNED_API_BASE_URL"]

    return get_functions_domain()


async def get_intuned_extension_settings(captcha_settings: CaptchaSolverSettings) -> dict[str, Any]:
    value = {
        **captcha_settings.model_dump(mode="json"),
        "workspaceId": get_workspace_id(),
        "projectId": get_project_id(),
        "authentication": get_intuned_extension_authentication().model_dump(),
        "baseUrl": get_intuned_base_url(),
    }
    return value


async def get_intuned_captcha_solver_settings() -> CaptchaSolverSettings:
    global captcha_settings
    if captcha_settings is not None:
        return captcha_settings
    intuned_json = await load_intuned_json()
    captcha_settings = (
        intuned_json.captcha_solver
        if intuned_json and intuned_json.captcha_solver is not None
        else CaptchaSolverSettings()
    )
    return captcha_settings


async def setup_intuned_extension():
    if not await is_intuned_extension_enabled():
        return
    captcha_settings = await get_intuned_captcha_solver_settings()
    await setup_intuned_extension_server(captcha_settings)
    settings_data = await get_intuned_extension_settings(captcha_settings)
    await write_intuned_extension_settings(settings_data)


async def write_intuned_extension_settings(settings: dict[str, Any]):
    intuned_extension_path = get_intuned_extension_path()
    if intuned_extension_path is None:
        raise RuntimeError("Intuned extension is not enabled")
    settings_path = intuned_extension_path / "intunedSettings.json"
    try:
        with open(settings_path, "w") as f:
            json.dump(settings, f)
    except Exception as e:
        raise RuntimeError(f"Failed to write settings to {settings_path}: {e}") from e


async def set_auto_solve(
    context: BrowserContext,
    enabled: bool,
) -> None:
    """
    Set the autoSolve setting in the browser extension service worker.

    Args:
        context: Playwright BrowserContext
        enabled: True to enable autoSolve, False to disable

    Raises:
        RuntimeError: If service worker not found or update fails
    """
    service_worker = await get_intuned_worker(context)
    if service_worker is None:
        if not enabled:  # If we are willing to pause the solving, and the worker is not available we are not gonna solve so we can exit
            return
        raise RuntimeError("Intuned service worker not found")

    # Update autoSolve directly in chrome.storage.local
    await service_worker.evaluate(
        """
        (enabled) => new Promise((resolve, reject) => {
            const updateSettings = () => {
                if (chrome?.storage?.local) {
                    chrome.storage.local.get('settings', (result) => {
                        if (chrome.runtime.lastError) {
                            reject(new Error(chrome.runtime.lastError.message));
                            return;
                        }
                        console.log(result.settings);
                        const settings = result.settings || {};
                        if (!settings.settings) {
                            settings.settings = {};
                        }
                        settings.settings.autoSolve = enabled;
                        console.log(settings);
                        chrome.storage.local.set({ settings }, () => {
                            if (chrome.runtime.lastError) {
                                reject(new Error(chrome.runtime.lastError.message));
                            } else {
                                resolve(true);
                            }
                        });
                    });
                } else {
                    setTimeout(updateSettings, 50);
                }
            };
            updateSettings();
        })
    """,
        enabled,
    )

    logger.debug(f"Set autoSolve to {enabled}")


async def get_worker_extension_settings(context: BrowserContext) -> dict[str, Any]:
    """
    Get current captcha solver settings from the browser extension service worker.

    Args:
        context: Playwright BrowserContext

    Returns:
        Dictionary containing current extension settings

    Raises:
        RuntimeError: If service worker not found or settings cannot be retrieved
    """
    service_worker = await get_intuned_worker(context)
    if service_worker is None:
        raise RuntimeError("Intuned service worker not found")

    # Read from chrome.storage.local
    settings = await service_worker.evaluate("""
        () => new Promise((resolve, reject) => {
            // Wait for chrome.storage.local to be available
            const checkStorage = () => {
                if (chrome?.storage?.local) {
                    chrome.storage.local.get('settings', (result) => {
                        if (chrome.runtime.lastError) {
                            reject(new Error(chrome.runtime.lastError.message));
                        } else {
                            resolve(result.settings || {});
                        }
                    });
                } else {
                    // Retry after a short delay
                    setTimeout(checkStorage, 50);
                }
            };
            checkStorage();
        })
    """)

    return settings


def set_captcha_solver_settings(captcha_solver_settings: CaptchaSolverSettings) -> None:
    global captcha_settings
    captcha_settings = captcha_solver_settings


async def update_captcha_solver_settings(
    context: BrowserContext,
    captcha_solver_settings: CaptchaSolverSettings,
) -> None:
    """
    Update the browser extension service worker's settings with new CaptchaSolverSettings.

    This replaces the entire settings object in chrome.storage.local with the
    serialized CaptchaSolverSettings.

    Args:
        context: Playwright BrowserContext
        captcha_solver_settings: CaptchaSolverSettings instance to write to storage

    Raises:
        RuntimeError: If service worker not found or update fails
    """
    global captcha_settings
    service_worker = await get_intuned_worker(context)
    if service_worker is None:
        raise RuntimeError("Intuned service worker not found")

    settings_dict = await get_intuned_extension_settings(captcha_solver_settings)

    await service_worker.evaluate(
        """
        (settings) => new Promise((resolve, reject) => {
            const updateStorage = () => {
                if (chrome?.storage?.local) {
                    chrome.storage.local.set({ settings }, () => {
                        if (chrome.runtime.lastError) {
                            reject(new Error(chrome.runtime.lastError.message));
                        } else {
                            resolve(true);
                        }
                    });
                } else {
                    setTimeout(updateStorage, 50);
                }
            };
            updateStorage();
        })
    """,
        settings_dict,
    )
    set_captcha_solver_settings(captcha_solver_settings)
    logger.debug("Updated captcha solver settings in chrome.storage.local")
