from dataclasses import dataclass, field
from typing import List, Set

from nirukta.models.gloss import EnglishGloss, Gloss


@dataclass
class SimpleToken:
    """An unanalysed Sanskrit word with its glosses."""

    slp1: str
    glosses: List[Gloss] = field(default_factory=list)

    def gloss_refs(
        self, english: str, visited: Set[tuple[int, int]]
    ) -> List[tuple[int, int]]:
        gloss_refs: List[tuple[int, int]] = []
        for gloss in self.glosses:
            if isinstance(gloss, EnglishGloss):
                ref = gloss.find_reference(english, visited)
                visited.add(ref)
                gloss_refs.append(ref)

        return gloss_refs
