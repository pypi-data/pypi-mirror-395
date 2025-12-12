from .intuned_extension import get_intuned_extension_path
from .intuned_extension import is_intuned_extension_loaded


def build_extensions_list() -> list[str]:
    extensions_list: list[str] = []

    if is_intuned_extension_loaded():
        intuned_extension_path = get_intuned_extension_path()
        extensions_list.append(str(intuned_extension_path))
    return extensions_list
