import os

from runtime.context.context import IntunedContext


def setup_ide_functions_token():
    ide_functions_token = os.getenv("INTUNED_AUTHORING_SESSION_BACKEND_FUNCTIONS_TOKEN")
    if ide_functions_token is None:
        return
    IntunedContext.current().functions_token = ide_functions_token
