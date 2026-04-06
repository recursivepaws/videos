from dataclasses import dataclass
from typing import List, Optional

from nirukta.constants import DIGITS_RE

from nirukta.models.presentation.line import Line


@dataclass
class Sloka:
    """"""

    lines: List[Line]
    number: Optional[int]

    def __init__(self, lines: List[Line]) -> None:
        number = None
        for line in list(lines):
            for vAyka in line.vAkyAni:
                for token in vAyka.tokens:
                    if isinstance(token, str):
                        if match := DIGITS_RE.search(token):
                            number = int(match.group())
        self.lines = lines
        self.number = number

        pass
