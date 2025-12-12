import importlib.util
import os
import sys

from runtime.env import get_browser_type


def _load_playwright_patch_function():
    """
    Dynamically load the setup_playwright_alias function.
    First checks PLAYWRIGHT_PATCH_SCRIPT_PATH env var for a custom script path.
    Falls back to the default intuned_cli.utils.patch_playwright module.
    """
    custom_script_path = os.environ.get("PLAYWRIGHT_PATCH_SCRIPT_PATH")

    if custom_script_path:
        # Load from custom path
        if not os.path.exists(custom_script_path):
            return None

        try:
            # Load the module from file path
            spec = importlib.util.spec_from_file_location("custom_patch_playwright", custom_script_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules["custom_patch_playwright"] = module
                spec.loader.exec_module(module)

                if hasattr(module, "setup_playwright_alias"):
                    return module.setup_playwright_alias
                else:
                    return None
        except Exception:
            return None


def setup_stealth_if_enabled():
    # Load Intuned settings to check if stealth mode is enabled
    try:
        from runtime.run.intuned_settings import load_intuned_settings_sync

        settings = load_intuned_settings_sync()
        if settings.stealth_mode.enabled:
            # Only patch playwright if stealth mode is enabled
            setup_playwright_alias = _load_playwright_patch_function()
            browser_type = get_browser_type()
            if setup_playwright_alias and browser_type in ("chromium", "brave"):
                setup_playwright_alias()
    except Exception:
        # If we can't load settings, don't patch (default behavior)
        pass
