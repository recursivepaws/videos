from dataclasses import dataclass
from typing import List
from nirukta.models.presentation import Sloka


@dataclass
class SutraFile:
    citation: str
    slokas: List[Sloka]
