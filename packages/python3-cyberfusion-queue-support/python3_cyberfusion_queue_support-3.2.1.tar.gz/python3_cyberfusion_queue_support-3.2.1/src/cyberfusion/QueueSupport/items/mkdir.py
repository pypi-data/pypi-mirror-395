"""Item."""

import logging
import os
from pathlib import Path
from typing import List, Optional

from cyberfusion.QueueSupport.exceptions import (
    PathIsSymlinkError,
    PathIsFileError,
    ParentNotFoundError,
)
from cyberfusion.QueueSupport.items import _Item
from cyberfusion.QueueSupport.outcomes import MkdirItemCreateOutcome

logger = logging.getLogger(__name__)


class MkdirItem(_Item):
    """Represents item."""

    def __init__(
        self,
        *,
        path: str,
        recursively: bool = False,
        reference: Optional[str] = None,
        hide_outcomes: bool = False,
        fail_silently: bool = False,
    ) -> None:
        """Set attributes."""
        self.path = path
        self.recursively = recursively
        self._reference = reference
        self._hide_outcomes = hide_outcomes
        self._fail_silently = fail_silently

    @property
    def outcomes(self) -> List[MkdirItemCreateOutcome]:
        """Get outcomes of item."""
        outcomes = []

        path_elements = list(reversed(Path(self.path).parents))
        path_elements.append(Path(self.path))

        for path in path_elements:
            if os.path.islink(path):
                raise PathIsSymlinkError(str(path))
            elif os.path.isfile(path):
                raise PathIsFileError(str(path))
            elif os.path.isdir(path):
                continue

            if not self.recursively and str(path) != self.path:
                raise ParentNotFoundError(str(path))

            outcomes.append(MkdirItemCreateOutcome(path=str(path)))

        return outcomes

    def fulfill(self) -> List[MkdirItemCreateOutcome]:
        """Fulfill outcomes."""
        outcomes = self.outcomes

        for outcome in outcomes:
            os.mkdir(outcome.path)

        return outcomes

    def __eq__(self, other: object) -> bool:
        """Get equality based on attributes."""
        if not isinstance(other, MkdirItem):
            return False

        return other.path == self.path
