"""Exceptions."""

from dataclasses import dataclass
from typing import List

from cyberfusion.QueueSupport.items import _Item


class ItemError(Exception):
    pass


@dataclass
class PathIsSymlinkError(ItemError):
    path: str


@dataclass
class PathIsFileError(ItemError):
    path: str


@dataclass
class ParentNotFoundError(ItemError):
    parent: str


@dataclass
class CommandQueueFulfillFailed(Exception):
    item: _Item
    command: List[str]
    stdout: str
    stderr: str

    def __str__(self) -> str:
        return f"Command:\n\n{self.command}\n\nStdout:\n\n{self.stdout}\n\nStderr:\n\n{self.stderr}"
