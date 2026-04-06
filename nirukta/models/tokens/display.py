
from dataclasses import dataclass
from typing import List


@dataclass
class DisplayToken:
    """A single renderable unit at a given animation stage."""

    slp1: str
    color: str  # resolved from colorings
    children: List["DisplayToken"]  # empty => leaf (SimpleToken or punct)
    english_spans: List[tuple[int, int]]  # the spans this token is responsible for

    @property
    def is_leaf(self) -> bool:
        return not self.children

    def at_depth(self, depth: int) -> List["DisplayToken"]:
        if self.is_leaf or depth == 0:
            return [self]
        return [leaf for child in self.children for leaf in child.at_depth(depth - 1)]
