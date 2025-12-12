import os


def get_workspace_id():
    return os.environ.get("INTUNED_WORKSPACE_ID")


def get_project_id():
    return os.environ.get("INTUNED_INTEGRATION_ID", os.environ.get("INTUNED_PROJECT_ID"))


def get_functions_domain():
    return os.environ.get("FUNCTIONS_DOMAIN")


def get_browser_type():
    return os.environ.get("BROWSER_TYPE")


def get_api_key():
    return os.environ.get(api_key_env_var_key)


def get_is_running_in_cli():
    return os.environ.get(cli_env_var_key) == "true"


def get_is_auth_session_recorder_enabled():
    return os.environ.get("INTUNED_AUTH_SESSION_RECORDER_ENABLED") == "true"


cli_env_var_key = "INTUNED_CLI"
workspace_env_var_key = "INTUNED_WORKSPACE_ID"
project_env_var_key = "INTUNED_PROJECT_ID"
api_key_env_var_key = "INTUNED_API_KEY"
