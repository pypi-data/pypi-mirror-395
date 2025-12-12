from typing import NotRequired
from typing import TypedDict

from pydantic import BaseModel
from pydantic import RootModel


class FileSystemTree(RootModel[dict[str, "DirectoryNode | FileNode"]]):
    root: dict[str, "DirectoryNode | FileNode"]


class DirectoryNode(BaseModel):
    directory: "FileSystemTree"


class FileNodeContent(BaseModel):
    contents: str


class FileNode(BaseModel):
    file: "FileNodeContent"


FileSystemTree.model_rebuild()


class BaseExecuteCommandOptionsWithoutTrace(TypedDict):
    headless: bool
    timeout: float
    proxy: NotRequired[str | None]
    keep_browser_open: bool
    cdp_url: NotRequired[str | None]


class BaseExecuteCommandOptions(BaseExecuteCommandOptionsWithoutTrace):
    trace: bool
