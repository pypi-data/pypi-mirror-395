import logging
import os
import sys

import arguably
from dotenv import find_dotenv
from dotenv import load_dotenv

import intuned_cli.commands  # pyright: ignore[reportUnusedImport] # noqa: F401
from intuned_cli.utils.error import CLIExit
from runtime.context.context import IntunedContext

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logging.getLogger().setLevel(logging.WARNING)
logging.getLogger("runtime").setLevel(logging.INFO)
logging.getLogger("intuned_runtime").setLevel(logging.INFO)
logging.getLogger("intuned_browser").setLevel(logging.INFO)


def run():
    dotenv = find_dotenv(usecwd=True)
    if dotenv:
        load_dotenv(dotenv, override=True)
        from runtime.env import cli_env_var_key

        os.environ[cli_env_var_key] = "true"
        os.environ["RUN_ENVIRONMENT"] = "AUTHORING"

        if not os.environ.get("FUNCTIONS_DOMAIN"):
            from intuned_cli.utils.backend import get_base_url

            os.environ["FUNCTIONS_DOMAIN"] = get_base_url().replace("/$", "")
    try:
        with IntunedContext():
            arguably.run(name="intuned", output=sys.stderr)
            return 0
    except CLIExit as e:
        return e.code


__all__ = ["run"]
