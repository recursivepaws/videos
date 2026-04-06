from dataclasses import dataclass
from typing import List

from nirukta.models.tokens import TokenType


@dataclass
class Utterance:
    """One sentence-worth of Sanskrit tokens paired with its English rendering."""

    tokens: List[TokenType]
    english: str
