from dataclasses import dataclass, field
from typing import List, Optional, Union

from nirukta.models.tokens.simple import SimpleToken
from nirukta.models.gloss import EtymGloss


@dataclass
class CompoundToken:
    """A sandhi compound.

    parts   -- ordered list of SimpleToken / CompoundToken (the components)
    slp1 -- the phonetically-merged SLP1 surface form (after '=')
    """

    parts: List[Union[SimpleToken, "CompoundToken"]]
    slp1: str
    etym_gloss: Optional[EtymGloss] = field(default=None)
