from dataclasses import dataclass
from typing import List

from nirukta.models.presentation.utterance import Utterance


@dataclass
class Line:
    """A stanza-level grouping of verse lines (between --- line --- markers)."""

    vAkyAni: List[Utterance]
